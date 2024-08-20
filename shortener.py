import pyshorteners

link = input("Enter the link to the Fabula Scoreboard: ")
shortner = pyshorteners.Shortener()
print(shortner.tinyurl.short(link))