import time

class TuringMachine:
    def __init__(self, tape="", blank_symbol=" ", initial_state="", final_states=None, transition_function=None):
        self.tape = list(tape)
        self.blank_symbol = blank_symbol
        self.head_position = 0
        self.current_state = initial_state
        self.final_states = final_states if final_states else set()
        self.transition_function = transition_function if transition_function else {}
        self.step_counter = 0

    def step(self):
        if self.current_state in self.final_states:
            return False 

        # extend tape if needed
        if self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)

        current_symbol = self.tape[self.head_position]
        key = (self.current_state, current_symbol)

        if key in self.transition_function:
            new_state, new_symbol, direction = self.transition_function[key]
            
            self.tape[self.head_position] = new_symbol
            self.current_state = new_state
            
            # Move head
            if direction == 'R':
                self.head_position += 1
            elif direction == 'L':
                self.head_position -= 1
            
            self.step_counter += 1
            # Uncomment for debug:
            # self.print_tape()
            return True
        else:
            print(f"Halted at state '{self.current_state}' with symbol '{current_symbol}' at position {self.head_position}")
            return False

    def print_tape(self):
        # Convert list to string and strip trailing blanks for display
        tape_str = "".join(self.tape).rstrip()
        print(f"Step {self.step_counter}: {tape_str}")

# Machine to generate 0 1 0 1 1 0 1 1 1 0 1 1 1 1 ...
# This number (Liouville-like constant) is irrational.

transitions = {
    # -- Initial Sequence Setup --
    # Start: [ ] -> 0 [ ]
    ('s_start', ' '): ('s_step1', '0', 'R'),
    
    # Step1: 0 [ ] -> 0 1 [ ]
    ('s_step1', ' '): ('s_step2', '1', 'R'),
    
    # Step2: 0 1 [ ] -> 0 1 0 (Head stays on the 0)
    ('s_step2', ' '): ('s_step3', '0', 'N'), # Stay on 0 to start scanning left logic properly?
                                              # Actually, let's fix the logic below.
    # Logic fix:
    # After writing 0 at end, we want to scan LEFT for 1s.
    # So head should move Left from the new 0.
    
    # Correcting s_step2 to move Left as before:
    ('s_step2', ' '): ('scan_left', '0', 'L'), # Directly go to scan_left state.
                                                # New tape: 0 1 0. Head is at '1'.
                                                # scan_left state handles '1' by marking it. Perfect.

    # -- Scanning Left for 1s to copy --
    # If we see a 1, mark it as x and go copy it.
    ('scan_left', '1'): ('mark_x', 'x', 'R'),
    
    # If we see an x, it's already copied, keep going left.
    ('scan_left', 'x'): ('scan_left', 'x', 'L'),
    
    # If we see a 0, we hit the previous block finish. Done copying 1s.
    ('scan_left', '0'): ('add_extra', '0', 'R'),
    
    # If we see blank (beginning of tape), done copying (first block case)
    ('scan_left', ' '): ('add_extra', ' ', 'R'), 

    # -- Copying Routine: mark_x --
    # We just marked a 1 as x. Go Right until we find empty spot.
    ('mark_x', 'x'): ('mark_x', 'x', 'R'),
    ('mark_x', '0'): ('seek_end', '0', 'R'),
    ('mark_x', '1'): ('mark_x', '1', 'R'), 
    
    # seek_end: Go past the current separator and any new 1s to find blank.
    ('seek_end', '1'): ('seek_end', '1', 'R'),
    ('seek_end', ' '): ('write_copy', '1', 'L'), # Write the 1. Return.

    # -- Returning Routine: write_copy --
    # Go Left back to the x.
    ('write_copy', '1'): ('write_copy', '1', 'L'),
    ('write_copy', '0'): ('return_to_src', '0', 'L'), # Cross separator Left
    
    ('return_to_src', '1'): ('return_to_src', '1', 'L'), # Skip any unmarked 1s
    ('return_to_src', 'x'): ('scan_left', 'x', 'L'),     # Found our x! Move Left to find NEXT 1.
    
    # -- Phase: add_extra --
    # We hit the left 0 boundary. Now we need to add one extra 1 at the end.
    # Tape: ... 0 x x x 0 1 1 1 [ ]
    
    ('add_extra', 'x'): ('add_extra', 'x', 'R'),   # Pass all the xs we made
    ('add_extra', '0'): ('go_finish', '0', 'R'),   # Cross the working separator
    ('add_extra', ' '): ('go_finish', ' ', 'R'),    # Handle blank start case if needed

    ('go_finish', '1'): ('go_finish', '1', 'R'),    # Pass all newly copied 1s
    ('go_finish', ' '): ('write_final', '1', 'L'),  # Write the N+1 th 1.
    
    # -- Cleanup Phase: Restore x -> 1 --
    # Navigate Left restoring xs.
    # From 'write_final', we are at the last 1. Go left.
    ('write_final', '1'): ('cleanup_scan', '1', 'L'),
    
    ('cleanup_scan', '1'): ('cleanup_scan', '1', 'L'), # Skip recently restored 1s on right
    ('cleanup_scan', '0'): ('cleanup_scan_left_side', '0', 'L'), # Cross separator Left
    
    ('cleanup_scan_left_side', '1'): ('cleanup_scan_left_side', '1', 'L'), # standard 1s
    ('cleanup_scan_left_side', 'x'): ('cleanup_scan_left_side', '1', 'L'), # Restore x to 1! Keep going Left.
    ('cleanup_scan_left_side', '0'): ('reset', '0', 'R'),        # Hit the Left 0. Cleanup done.
    ('cleanup_scan_left_side', ' '): ('reset', ' ', 'R'),        # Hit start of tape. Cleanup done.
    
    # -- Reset for next cycle --
    # We are at Left 0. Tape: ... 0 1 1 1 [0] 1 1 1 1 . (Actually head is on the 0, moving R)
    # We need to move to the far right, write 0, and start over.
    
    ('reset', '1'): ('reset', '1', 'R'), # Move past "old" block
    ('reset', '0'): ('reset_seek_end', '0', 'R'), # Found the separator (the one we just built off)
    ('reset', ' '): ('reset_seek_end', ' ', 'R'), # Case for very first block where left is blank
    
    ('reset_seek_end', '1'): ('reset_seek_end', '1', 'R'), # Move past "new" block
    ('reset_seek_end', ' '): ('scan_left', '0', 'L'), # Write new 0. Start scanning left immediately.
}

tm = TuringMachine(initial_state='s_start', transition_function=transitions)

print("Computing irrational number sequence (0 1 0 1 1 0 1 1 1 ...)")
start_time = time.time()
for i in range(5000): # Run for limit steps
    if not tm.step():
        break
end_time = time.time()

# Final tape output
print("\nFinal Tape Segment:")
final_tape = "".join(tm.tape).strip()
print(final_tape)
print(f"Length: {len(final_tape)}")
print(f"Steps: {tm.step_counter}")
print(f"Time: {end_time - start_time:.4f}s")