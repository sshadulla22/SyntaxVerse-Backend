# Troubleshooting Guide - ANCText Notes System

## Quick Status Check

### ✅ Backend is Running
Your backend logs show successful API calls, which means:
- Database is working
- API endpoints are responding
- CORS is configured correctly

### Check Frontend

1. **Open your browser to:** http://localhost:3000
2. **You should see:** Main page with a sidebar for creating topics

---

## Common Issues & Solutions

### Issue 1: "No topics showing on Main page"
**Solution:** You need to create topics first!
1. In the left sidebar, enter a topic name (e.g., "Python")
2. Click "Create Topic"
3. The topic should appear in the grid

### Issue 2: "Can't click into folders"
**Check:** Make sure you're clicking on the topic card, not just hovering
**Expected:** Clicking should navigate to `/notes/:id` URL

### Issue 3: "404 errors in console"
**Check:** Open browser DevTools (F12) and look at Console tab
**Solution:** If you see 404 errors, the backend might not be running on port 8000

### Issue 4: "CORS errors"
**Symptom:** Console shows "blocked by CORS policy"
**Solution:** Backend should already have CORS configured for localhost:3000
**Verify:** Check that backend main.py has the CORS middleware

### Issue 5: "Notes not saving"
**Steps to test:**
1. Create a topic on Main page
2. Click into the topic
3. Create a note
4. Click on the note
5. Click "Edit"
6. Add content
7. Click "Save"
**Expected:** Should show "Note saved successfully!" alert

---

## Testing Workflow

### Step 1: Create Topics (Main Page)
```
1. Go to http://localhost:3000
2. Enter "Python" in the input field
3. Click "Create Topic"
4. Repeat for "JavaScript", "Java"
```

### Step 2: Navigate into Topic
```
1. Click on "Python" topic card
2. URL should change to /notes/1
3. Breadcrumb should show: Home / Python
```

### Step 3: Create Folders and Notes
```
1. Enter "Basics" in the input field
2. Click "+ Folder" button
3. Enter "Variables" in the input field  
4. Click "+ Note" button
```

### Step 4: Navigate and Edit
```
1. Click into "Basics" folder
2. Click on "Variables" note
3. Click "Edit" button
4. Add some content
5. Click "Save"
6. Click "Back" button
```

---

## Verify Backend API Directly

Open these URLs in your browser to test the API:

1. **Get all root notes:**
   http://localhost:8000/notes/

2. **API Documentation:**
   http://localhost:8000/docs

3. **Create a test note via API docs:**
   - Go to http://localhost:8000/docs
   - Find POST /notes/
   - Click "Try it out"
   - Enter JSON:
   ```json
   {
     "title": "Test Topic",
     "content": "",
     "is_folder": true,
     "parent_id": null
   }
   ```
   - Click "Execute"

---

## Check Browser Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for any red error messages
4. Common errors:
   - `Failed to fetch` - Backend not running
   - `CORS policy` - CORS misconfigured
   - `404 Not Found` - Wrong API endpoint

---

## Database Check

The SQLite database is located at:
`c:\Users\acer\Desktop\Projects-22-25\ANCText\backend\notes.db`

If you want to reset everything:
1. Stop the backend server
2. Delete `notes.db` file
3. Restart backend (it will recreate the database)

---

## What's Working (Based on Logs)

✅ Backend API is responding  
✅ Database operations are working  
✅ CRUD operations (Create, Read, Update, Delete) are functional  
✅ Folder navigation is working  
✅ Frontend is making API calls successfully  

The system appears to be **fully functional**!

---

## If You're Still Having Issues

Please provide:
1. What URL are you on? (e.g., http://localhost:3000)
2. What do you see on the screen?
3. Are there any error messages?
4. What happens when you try to create a topic?
5. Screenshot of browser console (F12 → Console tab)
