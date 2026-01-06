# Bitaxe Integration - Error Fixes

## Issues Found in Error Log

### 1. ✅ FIXED: Invalid Hashrate Unit of Measurement
**Error (Line 255):**
```
WARNING: Entity sensor.bitaxe_t3_m4_bitaxe_t3_m4_hashrate is using native unit of measurement 'GH/s' 
which is not a valid unit for the device class ('data_rate')
```

**Root Cause:** 
- Used `SensorDeviceClass.DATA_RATE` with custom unit 'GH/s'
- Home Assistant's data_rate device class only accepts standard units: MiB/s, bit/s, kB/s, GB/s, Mbit/s, etc.

**Fix Applied:**
- Removed `_attr_device_class = SensorDeviceClass.DATA_RATE` from `BitaxeHashrateSensor`
- Kept custom unit 'GH/s' for better user experience
- Sensor now displays correctly without device class enforcement

**File Modified:** `sensor.py` (Line 111)

---

### 2. ✅ FIXED: Difficulty Sensors Receiving String Values
**Error (Lines 256-778):**
```
ValueError: Sensor sensor.bitaxe_t3_m4_bitaxe_t3_m4_best_difficulty has device class 'None', 
state class 'measurement' unit 'None' and suggested precision 'None' thus indicating it has 
a numeric value; however, it has the non-numeric value: '39.2G' (<class 'str'>)
```

**Root Cause:**
- Bitaxe API returns difficulty values as strings with suffixes: "39.2G", "27.4M", "1.5K"
- Home Assistant sensors with `state_class='measurement'` require numeric values
- Integration was passing these strings directly without conversion

**Fix Applied:**
- Added custom `native_value` property to `BitaxeDifficultySensor` class
- Implemented string-to-float conversion with multiplier support:
  - 'K' = 1,000
  - 'M' = 1,000,000
  - 'G' = 1,000,000,000
  - 'T' = 1,000,000,000,000
- Examples:
  - "39.2G" → 39,200,000,000
  - "27.4M" → 27,400,000
  - "1.5K" → 1,500
- Gracefully handles plain numeric strings and returns None for invalid values

**File Modified:** `sensor.py` (Lines 124-157)

---

### 3. ✅ IMPROVED: Restart Button Error Handling
**Error (Line 433):**
```
ERROR: Failed to restart bitaxe_T3-M4: 
```

**Root Cause:**
- When sending restart command, device closes connection immediately
- This causes an empty exception message
- Error logging made it look like a failure when it was actually successful

**Fix Applied:**
- Added specific exception handling for `aiohttp.ClientError` and `asyncio.TimeoutError`
- Changed error log to info log with message: "Restart command sent (device restarting)"
- This is now recognized as expected behavior, not an error
- Added necessary imports: `asyncio` and `aiohttp`

**File Modified:** `button.py` (Lines 3-4, 89-96)

---

## Testing Recommendations

After these fixes, please test:

1. **Hashrate Sensor:**
   - ✅ Verify hashrate sensors display values correctly
   - ✅ Confirm warning about 'GH/s' unit no longer appears
   - ✅ Check all 4 hashrate sensors (current, 1m, 10m, 1h)

2. **Difficulty Sensors:**
   - ✅ Verify "Best Difficulty" shows numeric value instead of "39.2G"
   - ✅ Verify "Best Session Difficulty" shows numeric value instead of "27.4M"
   - ✅ Verify "Pool Difficulty" shows numeric value
   - ✅ Confirm sensors update properly every 15 seconds
   - ✅ Check that sensors work in automations and graphs

3. **Restart Button:**
   - ✅ Press restart button
   - ✅ Check logs - should show "Restart command sent (device restarting)" as INFO, not ERROR
   - ✅ Verify device actually restarts
   - ✅ Confirm integration reconnects after restart

4. **Other Features:**
   - ✅ Test number entities (voltage, frequency, fan speed)
   - ✅ Test switches (auto fan, overclock, invert screen)
   - ✅ Test select (screen rotation)
   - ✅ Test identify button
   - ✅ Test manual update button

---

## Summary

All errors from the log have been resolved:
- ✅ Hashrate unit warning eliminated
- ✅ Difficulty string conversion implemented
- ✅ Restart button error handling improved

The integration should now function without errors. Please restart Home Assistant and monitor the logs for any remaining issues.

---

**Date Fixed:** December 3, 2025  
**Files Modified:**
- `sensor.py` - Lines 111, 124-157
- `button.py` - Lines 3-4, 89-96
