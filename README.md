# flex_meal_tracker


To Do List:

MUST HAVE:
- Finalize login/signup form responsiveness

- Finalize dashboard snapshot calculations

- Add "BACK TO TOP" option on daily log and exercise pages

- Conditional on login/signup page, if logged in user navs to these pages they are not presented with login/signup pages (maybe a jinja session conditional to present the dashboard page)

- Clear session when cancelling form submissions (consider making a cancel/blah route for each cancel button to clear session and redirect appropriately)

NICE TO HAVE:
- Try using the {% include "htmlfilenamehere" %} for calendar and footer

- Add light/dark mode toggle to Account page

- Make the header sticky/shrink when scrolling down pages & use icons instead of words (or, at the very least, add a "back to top" floating button on the daily tracker page)

- Upon sign-up, redirect to Account Page with banner/alert to setup initial weight/measurements (only present to user if this data doesn't exist in the db yet)

- Graphs in python to display in a dashboard/stats page
    (show weight over time and display target/goal weight)
    (show how many inches lost over time)

- Turn "?" help text into alert/pop up with password requirements (might look better HTML formatted)

- Allow users to upload an account/profile image



