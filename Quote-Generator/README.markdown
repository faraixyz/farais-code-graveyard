# Quote Generator
**Note: This repository is no longer being maintained.**
![A screenshot of Quote Generator](quote-generator-screenshot.png)

A website that generates quotes from [Epic Quotes](https://epicquotes.org). Not much to it besides that. This project was designed on [Codepen](https://codepen.io/fgandiya/full/zyNgPz), where you can also find a live version of this project. You can also clone or download this project and view it by opening the `index.html` file.

To set this project up yourself and host it on CodePen, do the following.

1. [Create a new pen in CodePen](https://codepen.io/pen/) and make sure you are in **Editor View**.
2. Copy the text in [`quotes.html`](quotes.html) into the HTML section of the editor.
3. Copy the text in [`script.js`](script.js) into the JavaScript section of the editor.
4. Copy the text in [`style.css`](style.css) into the CSS section of the editor.
5. Navigate to **Settings**. There, select **HTML**.
6. Copy the text from [`scripts`](scripts) and [`style`](style) into the box under **Stuff for &lt;head&gt;** and select **Save &amp; Close**.

Optionally, to get new quotes, do the following,
1. Ensure that Python 2 is installed on your computer.
2. In the command line, run `pip install bs4`. 
3. Download the [`Quotes.py`](Quotes.py) file.
4. In [`Quotes.py`](Quotes.py), you can modify the number of times you want to fetch quotes by modifying the `how_many` variables.
5. Run the script.
6. In the `q.txt` file located in the same directory as your script, copy all it's contents and paste them into the `quotes` variable. Be warned. It's massive.
