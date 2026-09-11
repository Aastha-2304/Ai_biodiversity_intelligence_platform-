import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app_streamlit_final.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The function render_health_gauge_svg and helper functions are defined in the
# MIDDLE of the if/elif chain. They need to be moved BEFORE the chain starts.

fn_start_marker = '\ndef render_health_gauge_svg(score: float, status_label: str) -> str:'
elif_marker = '\nelif active_panel == "\U0001f4ca Intelligence Dashboard":'
if_marker = '\nif active_panel == "\U0001f52c AI Scientist & Assessment":'

fn_start = content.find(fn_start_marker)
elif_pos = content.find(elif_marker)
if_pos = content.find(if_marker)

print(f'fn_start={fn_start}, elif_pos={elif_pos}, if_pos={if_pos}')

if fn_start != -1 and elif_pos != -1 and fn_start < elif_pos:
    # The misplaced block = from fn_start_marker to elif_marker (exclusive)
    misplaced_block = content[fn_start:elif_pos]
    print(f'Misplaced block: {len(misplaced_block)} chars')

    # Remove misplaced block from its current location, keeping elif
    content_without_misplaced = content[:fn_start] + content[elif_pos:]

    # Now re-find if_pos in the cleaned content
    if_pos2 = content_without_misplaced.find(if_marker)
    print(f'if_pos in cleaned content: {if_pos2}')

    if if_pos2 != -1:
        # Insert misplaced block BEFORE the if chain
        corrected = (
            content_without_misplaced[:if_pos2]
            + misplaced_block
            + '\n'
            + content_without_misplaced[if_pos2:]
        )
        with open('app_streamlit_fixed.py', 'w', encoding='utf-8') as out:
            out.write(corrected)
        print(f'Written app_streamlit_fixed.py: {len(corrected)} chars')
    else:
        print('ERROR: could not find if active_panel in cleaned content')
else:
    print('Could not find markers. fn_start:', fn_start, 'elif_pos:', elif_pos)
