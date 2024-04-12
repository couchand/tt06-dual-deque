## How it works

Each stack is an array of flip flops with a pointer to the top.  The empty and full
status flags are directly output, and push, pop, and the data bus lines are multiplexed
between the two stacks with the stack select line.

## How to test

To push (if `full` is low):

- Put the data byte on `data_in`
- Select which stack to push to with `stack_select`
- Bring `push` high for one cycle

To pop (if `empty` is low):

- Select which stack to pop with `stack_select`
- Bring `pop` high for one cycle

To read the top of stack:

- Select which stack to read with `stack_select`
- Wait one cycle
- Read top of stack from `data_out`
