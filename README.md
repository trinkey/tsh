# command-line
it's like bash but i made it

## !! VERY WIP !!

how to use:
1. download the code
2. install libraries if you haven't already (`pip install --upgrade dotindex readchar`)
3. run main.py
4. profit

## known issues
- the cursor position on the first line when there are multiple lines is off by one

## roadmap
(assuming i don't get distracted)
1. finish the text engine
   - [x] delete
   - [x] left
   - [x] right
   - [x] home
   - [x] end
   - [ ] up
   - [ ] down
   - [ ] tab (maybe wait until after implementing some commands?)
2. implement basic commands
   - [ ] ls (kinda works?)
   - [ ] cd
   - [ ] cat
   - [ ] echo
   - [ ] touch/mkdir
   - [ ] mv/cp
3. detect executables in `/bin/...`, `/usr/bin/...`, etc. and allow running them
4. piping and that kinda stuff
   - [ ] ... | ... (also add grep)
   - [ ] ... > ... (write to file)
   - [ ] ... >> ... (append to file)
5. math
   - [ ] +/-
   - [ ] */[division\]/%/^ (maybe use ** for exponents like python?)
   - [ ] parenthesis and order of operations
   - [ ] bitwise operators
7. variables
8. add the programming language part
   - [ ] if/else
   - [ ] while
   - [ ] for
