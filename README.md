The updated code is - `Solution_v5.py`
How to run - `python3  Solution_v5.py ./inputs/e_also_big.in`

## The solution outline

`Solution_v5.py` This is a **hybrid** solution. This solution could give you an **optimal** result.

- **Step 1:** The program will scan the input `pizza_types` from the left side (in decreasing order) and forms a greedy solution that can provide **total slice ordered less than max slice required**. Let the output set of pizza types be `pizza_types_orderd_greedy` and remaining pizza slice to be ordered is `order_remaining`. See the `greedySolution()` method of `Solution_v5.py`.

- **Step 2:** The program will scan the input pizza types from the right side (in increasing order) and feed it to dynamic programing(DP) solution. The input to the DP is `order_remaining` and `pizza_types`. Let the output set of pizza types be `pizza_types_orderd_dp`. See the `dynamicSolution()` method of `Solution_v5.py`. 

- **Step 3:** Add the output set of **Step 1:** and **Step 2:** i.e `pizza_types_orderd_dp + pizza_types_orderd_greedy` to get the **optimal** result. 