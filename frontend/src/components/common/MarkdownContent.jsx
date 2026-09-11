import React from 'react';

/**
 * Universal Markdown renderer for Darukaa AI.
 * Prevents double-bullets (• • or - •), properly renders numbered (<ol>) and unordered (<ul>)
 * lists, nested lists, headers, alerts, code, and tables without raw syntax leakage.
 */

function cleanBulletText(text) {
  // Strip combinations of bullet markers like '- •', '* •', '• •', '•', '-', '*'
  return text
    .replace(/^(\s*[-*•–]\s*)+/g, '')
    .trim();
}

function inlineFormat(text) {
  if (!text) return null;
  const parts = [];
  // Matches `code`, **bold**, *italic*, [link](url), or bracketed tags
  const regex = /(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*|\[([^\]]+)\]\(([^)]+)\)|\[([^\]]+)\])/g;
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }
    const full = match[0];
    if (full.startsWith('`')) {
      parts.push(<code key={match.index} className="md-code">{full.slice(1, -1)}</code>);
    } else if (full.startsWith('**')) {
      parts.push(<strong key={match.index} className="md-strong">{full.slice(2, -2)}</strong>);
    } else if (full.startsWith('*')) {
      parts.push(<em key={match.index} className="md-em">{full.slice(1, -1)}</em>);
    } else if (match[2] && match[3]) {
      parts.push(
        <a key={match.index} href={match[3]} target="_blank" rel="noreferrer" className="md-link">
          {match[2]}
        </a>
      );
    } else if (match[4]) {
      parts.push(<span key={match.index} className="md-tag">[{match[4]}]</span>);
    }
    lastIndex = match.index + full.length;
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }

  return parts.length > 0 ? parts : text;
}

export default function MarkdownContent({ text, className = '' }) {
  if (!text) return null;

  const rawLines = text.split('\n');
  const elements = [];

  let inCodeBlock = false;
  let codeBuffer = [];
  let codeLanguage = '';

  let inTable = false;
  let tableBuffer = [];

  let listBuffer = []; // { type: 'ul'|'ol', level: number, content: string, number?: number }

  const flushList = (keySuffix) => {
    if (listBuffer.length === 0) return;

    // Group items into list elements
    const renderedItems = [];
    let currentType = listBuffer[0].type;
    let group = [];

    const flushGroup = (gIdx) => {
      if (group.length === 0) return;
      if (currentType === 'ol') {
        renderedItems.push(
          <ol key={`list-${keySuffix}-${gIdx}`} className="md-ol">
            {group.map((item, idx) => (
              <li key={idx} className="md-li">
                {inlineFormat(item.content)}
              </li>
            ))}
          </ol>
        );
      } else {
        renderedItems.push(
          <ul key={`list-${keySuffix}-${gIdx}`} className="md-ul">
            {group.map((item, idx) => (
              <li key={idx} className={`md-li ${item.level > 0 ? 'md-li-nested' : ''}`}>
                {inlineFormat(item.content)}
              </li>
            ))}
          </ul>
        );
      }
      group = [];
    };

    listBuffer.forEach((item, idx) => {
      if (item.type !== currentType) {
        flushGroup(idx);
        currentType = item.type;
      }
      group.push(item);
    });
    flushGroup('last');

    elements.push(<div key={`lists-wrap-${keySuffix}`} className="md-list-wrapper">{renderedItems}</div>);
    listBuffer = [];
  };

  const flushTable = (keySuffix) => {
    if (tableBuffer.length === 0) return;
    const cleanRows = tableBuffer.filter(r => !r.match(/^[\s|:-]+$/));
    if (cleanRows.length === 0) {
      tableBuffer = [];
      inTable = false;
      return;
    }
    const headerCells = cleanRows[0].split('|').filter(c => c.trim().length > 0).map(c => c.trim());
    const bodyRows = cleanRows.slice(1);

    elements.push(
      <div key={`tbl-wrap-${keySuffix}`} className="md-table-wrapper">
        <table className="md-table">
          {headerCells.length > 0 && (
            <thead>
              <tr>
                {headerCells.map((h, i) => (
                  <th key={i}>{inlineFormat(h)}</th>
                ))}
              </tr>
            </thead>
          )}
          <tbody>
            {bodyRows.map((row, ri) => {
              const cells = row.split('|').filter(c => c.trim().length > 0).map(c => c.trim());
              return (
                <tr key={ri}>
                  {cells.map((c, ci) => (
                    <td key={ci}>{inlineFormat(c)}</td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
    tableBuffer = [];
    inTable = false;
  };

  rawLines.forEach((line, index) => {
    const trimmed = line.trim();

    // Check for fenced code blocks
    if (trimmed.startsWith('```')) {
      flushList(index);
      flushTable(index);
      if (inCodeBlock) {
        // closing code block
        elements.push(
          <pre key={`code-${index}`} className="md-code-block">
            <code>{codeBuffer.join('\n')}</code>
          </pre>
        );
        codeBuffer = [];
        inCodeBlock = false;
      } else {
        inCodeBlock = true;
        codeLanguage = trimmed.slice(3).trim();
      }
      return;
    }

    if (inCodeBlock) {
      codeBuffer.push(line);
      return;
    }

    // Check for table rows
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      flushList(index);
      inTable = true;
      tableBuffer.push(trimmed);
      return;
    }
    if (inTable) {
      flushTable(index);
    }

    // Empty line / spacer
    if (trimmed === '') {
      flushList(index);
      return;
    }

    // Horizontal rule
    if (/^(---|\*\*\*|___)$/.test(trimmed)) {
      flushList(index);
      elements.push(<hr key={`hr-${index}`} className="md-hr" />);
      return;
    }

    // Headers
    if (/^#{1,6}\s/.test(trimmed)) {
      flushList(index);
      const match = trimmed.match(/^(#{1,6})\s+(.*)$/);
      if (match) {
        const level = match[1].length;
        const headingText = match[2];
        const HeaderTag = `h${Math.min(level + 1, 6)}`; // h2-h6
        elements.push(
          <HeaderTag key={`h-${index}`} className={`md-header md-h${level}`}>
            {inlineFormat(headingText)}
          </HeaderTag>
        );
        return;
      }
    }

    // Blockquote & Alerts
    if (trimmed.startsWith('>')) {
      flushList(index);
      const quoteText = trimmed.replace(/^>\s*/, '');
      let alertType = null;
      let alertContent = quoteText;

      const alertMatch = quoteText.match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$/i);
      if (alertMatch) {
        alertType = alertMatch[1].toUpperCase();
        alertContent = alertMatch[2];
      }

      if (alertType) {
        elements.push(
          <div key={`alert-${index}`} className={`md-alert md-alert-${alertType.toLowerCase()}`}>
            <span className="md-alert-badge">{alertType}</span>
            <div className="md-alert-content">{inlineFormat(alertContent)}</div>
          </div>
        );
      } else {
        elements.push(
          <blockquote key={`quote-${index}`} className="md-blockquote">
            {inlineFormat(quoteText)}
          </blockquote>
        );
      }
      return;
    }

    // Numbered List: e.g. "1. " or "2) "
    const numberedMatch = trimmed.match(/^(\d+)[.)]\s+(.*)$/);
    if (numberedMatch) {
      const num = parseInt(numberedMatch[1], 10);
      const content = numberedMatch[2];
      listBuffer.push({
        type: 'ol',
        level: 0,
        number: num,
        content: cleanBulletText(content)
      });
      return;
    }

    // Bullet List: standard '-' or '*' or literal '•' or '–'
    // Also handles indent level (e.g. 2 or 4 spaces)
    const bulletMatch = line.match(/^(\s*)([-*•–]|(\*\s*•)|(-\s*•))\s+(.*)$/);
    if (bulletMatch) {
      const indent = bulletMatch[1].length;
      const level = Math.floor(indent / 2);
      const rawContent = bulletMatch[5];
      listBuffer.push({
        type: 'ul',
        level: level,
        content: cleanBulletText(rawContent)
      });
      return;
    }

    // Standalone literal bullet line (e.g. "• Option A") without space
    if (trimmed.startsWith('•') || trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      listBuffer.push({
        type: 'ul',
        level: 0,
        content: cleanBulletText(trimmed)
      });
      return;
    }

    // Default paragraph
    flushList(index);
    elements.push(
      <p key={`p-${index}`} className="md-p">
        {inlineFormat(trimmed)}
      </p>
    );
  });

  flushList('end');
  flushTable('end');

  if (inCodeBlock && codeBuffer.length > 0) {
    elements.push(
      <pre key="code-end" className="md-code-block">
        <code>{codeBuffer.join('\n')}</code>
      </pre>
    );
  }

  return <div className={`markdown-content ${className}`}>{elements}</div>;
}
