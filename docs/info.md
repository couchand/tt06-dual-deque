Two independent stacks in one tiny footprint.

## How it works

Each stack is an array of flip flops with a pointer to the top.  The empty and full
status flags for each are directly available on pins.  The push and pop inputs as
well as data bus lines are multiplexed using the stack select line.

## How to test

To push (if `full` is low):

- Put the data byte on `data_in`
- Select which stack to push to with `stack_select`
- Bring `push` high for one cycle

To pop (if `empty` is low):

- Select which stack to pop with `stack_select`
- Bring `pop` high for one cycle

To replace the top of the stack (if `empty` is low):

- Select which stack with `stack_select`
- Put the new data byte on `data_in`
- Bring both `push` and `pop` high for one cycle

To read the top of stack:

- Select which stack to read with `stack_select`
- Wait one cycle
- Read top of stack from `data_out`

## External hardware

You would probably want to connect this to other devices that would find it useful.
