# EventLog Blueprint - Installation & Testing Guide

Complete step-by-step guide to install EventLog blueprint and test basic functionality.

**Time Required**: 30-45 minutes

---

## Part 1: GitHub Push (5 minutes)

### Step 1: Push Updated Code to GitHub

```bash
cd /config/ClaudeProjects/EventLog
git add -A
git commit -m "refactor: Redesign EventLog as single Home Assistant Blueprint..."
git push origin main
```

### Step 2: Verify on GitHub

1. Open: https://github.com/Alvin366/EventLog
2. Verify:
   - ✅ `blueprints/` directory exists with 2 YAML files
   - ✅ `README.md` updated for blueprint approach
   - ✅ Old directories removed (custom_components, scripts, etc.)
   - ✅ Latest commit shows "refactor: Redesign"

---

## Part 2: Install Blueprint in Home Assistant (10 minutes)

### Step 1: Navigate to Blueprints

In Home Assistant:
1. Go to: **Settings → Automations & Scenes → Blueprints**
2. You should see a blue button: **"Import Blueprint"**

### Step 2: Import EventLog Master Blueprint

1. Click **"Import Blueprint"**
2. A dialog box appears asking for blueprint URL
3. Paste:
   ```
   https://github.com/Alvin366/EventLog/blob/main/blueprints/eventlog_master.yaml
   ```
4. Click **"Import Blueprint"**

**Expected result**:
- Blueprint shows in your blueprints list
- Shows name: "EventLog - Event Collector & Manager"
- You can now click "Create Automation"

### Step 3: Create Automation from Blueprint

1. Click **"Create Automation"** on EventLog blueprint
2. Configure with these settings:

   | Setting | Value |
   |---------|-------|
   | Automation name | EventLog Master |
   | Event Category | system |
   | Event Severity Level | minor |
   | Dedup Window | 5 (minutes) |
   | Enable Acknowledgment | ON |
   | Enable Closure | ON |
   | Archive After | 7 (days) |
   | Notify on Critical | OFF |

3. Click **"Create Automation"**

**Expected result**:
- Automation created successfully
- Shows as "EventLog Master" in automations list
- Status shows "ON" (enabled)

### Step 4: Verify Helpers Created

Home Assistant should automatically create helper entities:

1. Go to: **Settings → Devices & Services → Helpers**
2. Search for: `eventlog`
3. You should see:
   - ✅ `input_text.eventlog_active_events`
   - ✅ `input_text.eventlog_acknowledged_events`
   - ✅ `input_text.eventlog_archive`

**If helpers NOT created**:
- Create manually:
  1. Click "Create Helper" → "Text"
  2. Create these:
     - Name: "EventLog Active Events"
     - Entity ID: `eventlog_active_events`
     - Max length: 2048
     - Initial: `[]`
  3. Repeat for others

---

## Part 3: Test Basic Functionality (20 minutes)

### Test 1: Fire Test Event

**Goal**: Verify EventLog receives and stores events

1. Go to: **Developer Tools → Events**

2. Find the "Publish Event" section

3. Enter:
   ```
   Event type: eventlog.log_event
   ```

4. In the data field, paste:
   ```json
   {
     "category": "test",
     "title": "Test Event 1",
     "message": "Testing EventLog basic functionality",
     "dedup_key": "test_event_001"
   }
   ```

5. Click **"Publish event"**

**Expected result**:
- Event fires (no error)
- Check helpers to see event stored

### Test 2: Verify Event Stored

1. Go to: **Developer Tools → States**

2. Search for: `input_text.eventlog_active_events`

3. Click on entity to see full state

4. You should see JSON with your test event:
   ```json
   [
     {
       "id": "1730000000_5234",
       "category": "test",
       "severity": "minor",
       "title": "Test Event 1",
       "message": "Testing EventLog basic functionality",
       "timestamp": "2024-10-30T16:00:00",
       "first_occurrence": "2024-10-30T16:00:00",
       "last_occurrence": "2024-10-30T16:00:00",
       "count": 1,
       "dedup_key": "test_event_001",
       "status": "active"
     }
   ]
   ```

**If event not showing**:
- Check automation is enabled
- Check logs for errors: **Settings → System → Logs**
- Try publishing event again

### Test 3: Test Deduplication

**Goal**: Verify duplicate events are merged

1. Fire the SAME event again (within 5 minutes):
   - Go to **Developer Tools → Events**
   - Use same event data as Test 1
   - Publish event

2. Check `input_text.eventlog_active_events` state

**Expected result**:
- Same event NOT duplicated
- `count` field increased to 2
- `last_occurrence` timestamp updated
- `first_occurrence` unchanged

**Example**:
```json
{
  "id": "1730000000_5234",  // SAME ID
  "count": 2,               // INCREASED
  "first_occurrence": "2024-10-30T16:00:00",  // UNCHANGED
  "last_occurrence": "2024-10-30T16:05:00",   // UPDATED
}
```

### Test 4: Create Second Event (Different)

**Goal**: Verify multiple events stored

1. Fire a DIFFERENT event:
   ```json
   {
     "category": "devices",
     "title": "Test Event 2",
     "message": "This is a different event",
     "dedup_key": "test_event_002"
   }
   ```

2. Check `input_text.eventlog_active_events`

**Expected result**:
- Both events in the list
- Array has 2 items
- Each with unique `dedup_key`

### Test 5: Create Critical Event (with notifications OFF)

**Goal**: Verify severity handling

1. Fire a CRITICAL event:
   ```json
   {
     "category": "security",
     "severity": "critical",
     "title": "Critical Security Event",
     "message": "Unauthorized access attempt",
     "dedup_key": "security_critical_001"
   }
   ```

2. Check helper state

**Expected result**:
- Event stored with `severity: critical`
- Event appears in helper

### Test 6: Test with Custom Dedup Key

**Goal**: Verify deduplication key works

1. Fire two events with SAME dedup_key but different titles:
   ```json
   {
     "title": "First Title",
     "dedup_key": "same_key_001"
   }
   ```
   Then:
   ```json
   {
     "title": "Second Title",
     "dedup_key": "same_key_001"
   }
   ```

2. Check helpers

**Expected result**:
- Only ONE event entry (duplicate merged)
- `count: 2`
- Title from first event (unchanged)

---

## Part 4: Dashboard Display (5 minutes)

### Create Simple Dashboard Card

1. Go to your dashboard (or Valiug)

2. Click **"Edit Dashboard"**

3. Click **"Add Card"**

4. Choose **"Entities"**

5. Add these entities:
   ```
   - input_text.eventlog_active_events
   - input_text.eventlog_acknowledged_events
   - input_text.eventlog_archive
   ```

6. Click **"Save"**

**Expected result**:
- Card shows event list
- Displays JSON data
- Updates as events are added

### Create Better Display (Optional)

For cleaner display, create custom template card:

1. Click **"Add Card"** → **"Manual YAML"**

2. Paste:
   ```yaml
   type: custom:template-entity-row
   entity: input_text.eventlog_active_events
   name: Active Events
   content: |
     [[[
       try {
         const events = JSON.parse(entity_id('input_text.eventlog_active_events').state || '[]');
         return `${events.length} events`;
       } catch(e) {
         return 'Error parsing events';
       }
     ]]]
   ```

---

## Troubleshooting

### Blueprint Won't Import

**Problem**: "Failed to import blueprint" error

**Solution**:
1. Check URL is correct (copy from GitHub directly)
2. Check network connection
3. Try refresh browser
4. Check Home Assistant version is 2024.9.0+

### Automation Not Running

**Problem**: Event fires but nothing happens

**Solution**:
1. Verify automation is **Enabled** (toggle switch ON)
2. Check logs: **Settings → System → Logs**
3. Search for "eventlog" in logs
4. Verify event trigger matches: `eventlog.log_event`

### Helpers Not Created

**Problem**: Input_text helpers don't exist

**Solution**:
1. Create manually via **Settings → Devices & Services → Helpers**
2. Or wait for first event to trigger blueprint (should auto-create)
3. Check automation is enabled

### Events Not Storing

**Problem**: Event fires but helper stays empty

**Solution**:
1. Check helper initial value is `[]`
2. Verify helper exists
3. Check automation logs for errors
4. Try with simpler event data (just category, title, message)

### Can't See Event in States

**Problem**: Helper exists but can't see event data

**Solution**:
1. Go to **Developer Tools → States**
2. Search for exact entity ID
3. Click entity to see full state (not just friendly name)
4. Check JSON format is valid

---

## Success Criteria

✅ **Blueprint installed successfully**
- Blueprint appears in blueprints list
- Can create automation from it

✅ **Helpers auto-created**
- Three `input_text` helpers exist
- Initial values are `[]`

✅ **Event stored**
- Test event fires without errors
- Event appears in helper JSON

✅ **Deduplication works**
- Duplicate events merge
- Count increases
- Last occurrence updates

✅ **Multiple events work**
- Can store multiple events
- Each has unique ID
- Array grows as events added

✅ **Dashboard displays events**
- Card shows event list
- Displays JSON data
- Updates in real-time

---

## Next Steps

Once basic tests pass:

1. **Install Event Source Blueprint**
   - Import: `eventlog_event_source.yaml`
   - Create automations to send events
   - Monitor sensors/entities

2. **Create More Event Sources**
   - Battery monitoring
   - Device status
   - Custom alerts

3. **Add Dashboard Display**
   - Create custom card template
   - Parse and display events nicely
   - Add action buttons

4. **Explore Advanced Features**
   - Test acknowledgment/closure
   - Test archive functionality
   - Enable notifications

---

## Quick Checklist

```
Installation:
  ☐ GitHub push complete
  ☐ Blueprint imported
  ☐ Automation created
  ☐ Helpers created

Testing:
  ☐ Test event fires
  ☐ Event stored in helper
  ☐ Deduplication works
  ☐ Multiple events work
  ☐ Dashboard shows events

Next Phase:
  ☐ Event Source blueprint installed
  ☐ Custom event sources created
  ☐ Dashboard display improved
  ☐ Notifications tested
```

---

**Questions?** Check README.md or GitHub Issues.

**Ready?** Start with Part 1 - GitHub Push!

---

**Version**: 0.2.0-Blueprint-MVP
**Last Updated**: 2024-10-30
