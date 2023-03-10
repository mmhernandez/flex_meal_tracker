# flex_meal_tracker


To Do List:

MUST HAVE:
- Finalize login/signup form responsiveness

- Conditional on login/signup page, if logged in user navs to these pages they are not presented with login/signup pages (maybe a jinja session conditional to present the dashboard page)

- Clear session when cancelling form submissions (consider making a cancel/blah route for each cancel button to clear session and redirect appropriately)

- Make sure all files use the jinja url_for syntax for static file references

- Finalize readme


NICE TO HAVE:
- Get calendar to indicate what days have been filled out

- Try using the {% include "htmlfilenamehere" %} for calendar, scroll to top, and footer

- Add light/dark mode toggle to Account page

- Upon sign-up, redirect to Account Page with banner/alert to setup initial weight/measurements (only present to user if this data doesn't exist in the db yet)

- Turn "?" help text into alert/pop up with password requirements (might look better HTML formatted)



