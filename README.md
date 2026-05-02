========================================================================
🔍 FLOWLENS v2.1 - Visual Audit & Execution Tracing Tool
========================================================================

DESCRIPTION:
FlowLens is a Python tracing engine designed to audit the logical 
execution of algorithms. It transforms code execution into an 
interactive HTML report that allows you to visualize process flow, 
response times, and the nature of each operation.

Ideal for independent developers and researchers looking for a 
professional way to demonstrate how their systems work.

AUTHOR: Hans Saldias (Analyst Programmer)
STATUS: Proposal for the CPython Community

------------------------------------------------------------------------
✨ KEY FEATURES
------------------------------------------------------------------------

* CHRONOLOGICAL ORDER: Shows exactly where each process begins 
    (START) and ends (END).
* INTENT DETECTION: Automatically classifies if a function is an 
    "INTERNAL PROCESS / CALCULATION" or a "DATA OUTPUT".
* PERFORMANCE METRICS: Records exact execution time in 
    milliseconds (ms) for every block.
* DATA TRACEABILITY: Captures input arguments and return values 
    at every step.

------------------------------------------------------------------------
🚀 HOW TO USE FLOWLENS
------------------------------------------------------------------------

1. REQUIREMENTS:
   No external dependencies required. You only need to have the 
   `flowlens.py` file in your project folder.

2. QUICK IMPLEMENTATION:
   Import the `lens` object and use the `@lens.track_stats` decorator 
   on the functions you wish to audit.

   Example:
   
   from flowlens import lens

   @lens.track_stats
   def my_algorithm(value):
       # This will be detected as an internal calculation
       return value * 2

   @lens.track_stats
   def show_data(result):
       # This will be detected as a data output
       print(result)

   # Start capturing
   lens.start()
   
   # Execute logic
   res = my_algorithm(50)
   show_data(res)
   
   # Stop and generate report
   lens.stop()

3. RESULT:
   A file named `flowlens_report.html` will be generated and will 
   automatically open in your default web browser.

------------------------------------------------------------------------
📂 PROJECT FILES
------------------------------------------------------------------------

* flowlens.py       -> The core audit engine.
* test_auditoria_15.py -> Integration test script with 15 processes.
* README.txt        -> Usage instructions.

------------------------------------------------------------------------
"Code clarity is the foundation of a secure audit."
========================================================================
