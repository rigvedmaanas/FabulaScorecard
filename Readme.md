# Fabula Scorecard

1. Install all the dependencies
2. Follow the check list
3. Remember to create an ngrok account for web scoreboard. (The current url will not work for anyone else except me)

# Check List

- Open The Whole Fabula Scoreboard folder in PyCharm and VSCode
- In VSCode open the index.html and click on the "Go Live" button in the lower right corner.
- Type `ngrok http --domain=765373626613-12120895592731527066.ngrok-free.app 5500` into a terminal.
- Then go to `765373626613-12120895592731527066.ngrok-free.app` . This will be the web scoreboard url.
- OR `https://tinyurl.com/29aocpce`
- Make sure to connect the second monitor and make the second monitor the primary one.
- Make sure to run "client" first.
- Then choose the configuration "client" and run the file.
- When the window to be shown is prompted. The monitor with x != 0 and y != 0 must be selected. The index is given in the left hand side.
- Then choose the configuration "main" and run the file.
- When the window to be shown is prompted. The monitor with x = 0 and y = 0 must be selected. The index is given in the left hand side.
- Then choose the configuration "FlashMessage" and run the file.
- When the window to be shown is prompted. The monitor with x = 0 and y = 0 must be selected. The index is given in the left hand side.

Note: The code is quite bad. I personally don't like the way I have written it. I would refactor it if I am going to use it again. Need to OOP. Maybe not show schools which have scored only 0 and also add an option to delete a school. Use this only if you know how it works. To convert csv to json use the function `csv_to_json` in client.py. Happy programming 😄
