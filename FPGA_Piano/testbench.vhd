-- *** Test Bench - User Defined Section ***
tb : PROCESS
BEGIN
  -- System Reset
  pb_in(0) <= '1';
  wait for 50 ns;
  pb_in(0) <= '0';
  wait for 50 ns;

  -- C3
  pb_in <= "0000";
  switch_in <= "10000000";
  wait for 500 us;

  -- B3# = C4
  pb_in <= "0100";
  switch_in <= "00000010"; -- B3#
  wait for 500 us;

  -- A4
  pb_in <= "1000";
  switch_in <= "00000100";
  wait for 500 us;

  -- D3
  pb_in <= "0000";
  switch_in <= "01000000";
  wait for 500 us;

  -- G0#
  pb_in <= "0100";
  switch_in <= "00001000";
  wait for 500 us;

  -- F4#
  pb_in <= "1100";
  switch_in <= "00010000";
  wait for 500 us;
END PROCESS;
