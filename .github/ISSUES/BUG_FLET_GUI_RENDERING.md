# GUI Rendering Issue: Components Not Displaying on Flet Desktop

## Issue Title
`[BUG] Flet GUI Components Rendering as Blank White Screen - Container/Column Layout Not Visible`

## Description
The QuantInvest Suite GUI built with Flet 0.85.0 is not properly rendering components on the desktop application. When the application launches, the window shows either:
1. A white/gray blank screen with only the title bar visible
2. Partial rendering with only header visible but main content area remaining white

## Environment
- **Flet Version:** 0.85.0
- **flet-desktop Version:** 0.85.0
- **Python Version:** 3.14
- **OS:** Windows 11
- **Framework:** Flet (Desktop)

## Expected Behavior
The GUI should display:
- Header with "QuantInvest Suite" title and emoji (✓ Rendering correctly)
- Input section with CSV file picker, strategy dropdown, and capital input
- Control buttons (Execute and Clear)
- Results display cards (4 metric cards in 2x2 grid)
- Chart placeholder areas

## Actual Behavior
The entire main content area (build_main_content() Container) remains blank/white despite:
- Components being created without errors
- No exceptions thrown during build_page()
- page.update() being called
- All controls added to the page

## Key Findings
- Simple Flet test application with basic components **DOES render correctly** (test_flet.py works)
- Component objects are created successfully (verified with debug prints)
- The issue occurs when using nested Container + Column structures with custom components
- CustomButton, CustomTextField, and ResultMetric components may have styling issues causing render failures

## Root Cause Analysis (Preliminary)
The problem likely stems from:
1. **Container/Column nesting hierarchy** - Too many nested containers may be breaking layout
2. **Custom component styling** - ThemeColors or component properties may have invalid Flet values
3. **Component expansion** - `expand=True` properties may not be working correctly in nested structure
4. **Child component initialization** - ResultMetric or ChartPlaceholder may be initializing with None values

## Affected Files
- `src/python_pdm_template/gui/main.py` - Main application builder
- `src/python_pdm_template/gui/components.py` - Custom component classes
- `src/python_pdm_template/gui/charts.py` - Chart placeholders

## Reproduction Steps
1. Run `python run_app.py` from project root
2. Flet window opens with title "QuantInvest Suite"
3. Only header renders, main content area is blank/white
4. All input fields, buttons, and results cards are invisible

## Attempted Solutions
- Removed FilePicker from overlay
- Simplified component hierarchy
- Added explicit heights and widths
- Tested with native Flet components (ElevatedButton, TextField, Dropdown)
- All attempted fixes failed - blank screen persists

## Next Steps for Resolution
1. **Debug nested components individually** - Test each section (input, controls, results, charts) in isolation
2. **Verify ThemeColors values** - Ensure all color strings are valid hex codes
3. **Check Flet property compatibility** - Some properties like `border=` syntax may be version-specific
4. **Simplify component tree** - Reduce nesting depth from current 5-6 levels to 2-3 levels
5. **Use ft.run() instead of ft.app()** - Test if newer Flet execution method resolves rendering
6. **Check for circular references** - Ensure ChartManager and component dependencies don't cause initialization loops

## Related Issues
- Flet 0.80.0+ deprecated `ft.app()` in favor of `ft.run()` 
- Desktop view rendering differs from web view in Flet
- Custom component inheritance from ft.Container may have layout implications

## Commit Reference
- Commit: `6e1b9a6` - GUI interface initial implementation
- Branch: `daniel`

## Notes
- Application runs without throwing exceptions
- Exit code 0 on execution
- Window is interactive (can close, resize, focus)
- Only issue is component visibility/rendering

