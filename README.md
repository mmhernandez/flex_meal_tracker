# flex_meal_tracker


To Do List:

MUST HAVE:
- Find a way to incorporate the DELETE part of CRUD (maybe deleting a daily log - in case the user added info to the wrong day?)

- Finalize login/signup form responsiveness

NICE TO HAVE:
- Make the header sticky/shrink when scrolling down pages & use icons instead of words (or, at the very least, add a "back to top" floating button on the daily tracker page)

- Upon sign-up, redirect to Account Page with banner/alert to setup initial weight/measurements (only present to user if this data doesn't exist in the db yet)

- Graphs in python to display in a dashboard/stats page
    (show weight over time and display target/goal weight)
    (show how many inches lost over time)

- Conditional on login/signup page, if logged in user navs to these pages they are not presented with login/signup pages (maybe a jinja session conditional to present the dashboard page)

- Consider using M/F sex selection in the account to present info on the dashboard (use an API with AJAX to pull in helpful articles or motivational stuff and place on the dashboard)

- Turn "?" help text into alert/pop up with password requirements (might look better HTML formatted)

- Clear session when cancelling form submissions (consider making a cancel/blah route for each cancel button to clear session and redirect appropriately)

- Add light/dark mode toggle to Account page

- Allow users to upload an account/profile image



