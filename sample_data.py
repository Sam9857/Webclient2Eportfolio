"""60 quiz questions (no AI needed).

Each row is written as: category, level, question, RIGHT answer, [3 wrong answers], explanation.
The code at the bottom puts the right answer in position A, B, C, D in turn,
so exactly 15 correct answers fall on each letter.
level: "basic" = internship track, "advanced" = experienced track.
"""

CATEGORIES = ["Python", "Flask", "HTML & CSS", "SQL & Databases", "Git & Web", "DSA & CS"]

_ROWS = [
    # ---------------- Python ----------------
    ("Python", "basic", "Which Python data type is immutable?", "tuple", ["list", "dict", "set"],
     "Tuples cannot be changed after creation; lists, dicts and sets can."),
    ("Python", "basic", "Which keyword defines a function in Python?", "def", ["fun", "function", "define"],
     "Functions start with the def keyword, for example def add(a, b):."),
    ("Python", "basic", "What does [x * 2 for x in range(3)] produce?", "[0, 2, 4]", ["[2, 4, 6]", "[0, 1, 2]", "[0, 2, 4, 6]"],
     "range(3) gives 0, 1, 2 and each value is doubled, so the result is [0, 2, 4]."),
    ("Python", "basic", "Which block is used to handle an exception in Python?", "try / except", ["try / catch", "catch / throw", "on error / resume"],
     "Python uses try and except. Other languages use catch."),
    ("Python", "basic", "What does self represent inside a class method?", "The object the method is called on", ["The class itself", "The parent class", "A global variable"],
     "self is the current instance, so the method can read and change that object's data."),
    ("Python", "advanced", "What is a decorator in Python?", "A function that wraps another function to add behaviour", ["A style of comment", "A type of loop", "A class attribute"],
     "Decorators such as @login_required wrap a function and run extra code before or after it."),
    ("Python", "advanced", "What does *args collect in a function definition?", "Extra positional arguments as a tuple", ["Extra keyword arguments as a dict", "One list argument", "All global variables"],
     "*args gathers any extra positional arguments. **kwargs gathers keyword arguments."),
    ("Python", "advanced", "What is the difference between == and is?", "== compares values, is compares object identity", ["== compares identity, is compares values", "They are exactly the same", "is only works on strings"],
     "Two equal lists can be different objects: == is True, is is False."),
    ("Python", "advanced", "Which keyword turns a function into a generator?", "yield", ["return", "generate", "async"],
     "A function that uses yield returns values one at a time and remembers where it stopped."),
    ("Python", "basic", "What does 'with open(\"f.txt\") as f:' guarantee?", "The file is closed automatically when the block ends", ["The file is created if it is missing", "The file can only be read", "The file stays locked forever"],
     "A with block calls the cleanup code even if an error happens inside it."),

    # ---------------- Flask ----------------
    ("Flask", "basic", "Which Flask function builds a URL from a view function name?", "url_for()", ["redirect()", "route_url()", "link_to()"],
     "url_for('login') returns the URL of the login view, so links do not break when routes change."),
    ("Flask", "basic", "Which decorator connects a URL to a view function?", "@app.route()", ["@app.url()", "@app.view()", "@app.link()"],
     "@app.route('/path') registers the function below it as the handler for that path."),
    ("Flask", "basic", "Where does Flask look for HTML templates by default?", "The templates folder", ["The views folder", "The html folder", "The static folder"],
     "render_template() loads files from a folder named templates next to your app."),
    ("Flask", "basic", "Which object holds the data submitted in an HTML form?", "request.form", ["session.form", "response.data", "g.form"],
     "request.form behaves like a dictionary of the submitted form fields."),
    ("Flask", "basic", "What is session used for in Flask?", "Remembering data about a user between requests", ["Connecting to the database", "Rendering templates", "Compressing static files"],
     "The session stores small values, like the logged-in user id, in a signed cookie."),
    ("Flask", "basic", "What does flash() do?", "Stores a one-time message to show on the next page", ["Clears the browser cache", "Reloads the page", "Writes an error to the log"],
     "Flashed messages are read once with get_flashed_messages() and then disappear."),
    ("Flask", "advanced", "Why store passwords with generate_password_hash()?", "A hash cannot be reversed, so a leaked database does not reveal passwords", ["It makes login faster", "It encrypts the password so you can decrypt it later", "Flask will not start without it"],
     "Hashing is one-way. Login compares the hash of the typed password with the stored hash."),
    ("Flask", "advanced", "What is a Flask Blueprint?", "A way to organise routes into reusable modules", ["A database migration", "A template engine", "A testing tool"],
     "Blueprints let you split a big app into parts such as auth, notes and admin."),
    ("Flask", "basic", "Which status code should a view return when something is not found?", "404", ["200", "301", "500"],
     "404 means Not Found. 200 is success, 301 is a redirect and 500 is a server error."),
    ("Flask", "advanced", "Why is app.run(debug=True) unsafe on a public server?", "It exposes an interactive debugger that can run code", ["It disables sessions", "It turns off templates", "It makes the database slower"],
     "Debug mode shows the Werkzeug debugger. Anyone who reaches it can execute code on the server."),

    # ---------------- HTML & CSS ----------------
    ("HTML & CSS", "basic", "Which HTML5 element is best for the main navigation links?", "<nav>", ["<div>", "<section>", "<aside>"],
     "<nav> is the semantic element for major navigation blocks."),
    ("HTML & CSS", "basic", "Which CSS declaration turns an element into a flex container?", "display: flex", ["position: flex", "float: flex", "flex: container"],
     "display: flex enables the Flexbox layout for the element's children."),
    ("HTML & CSS", "basic", "Which attribute makes a form field mandatory?", "required", ["mandatory", "validate", "needed"],
     "The browser will not submit the form while a required field is empty."),
    ("HTML & CSS", "basic", "Which CSS selector targets the element with id=\"menu\"?", "#menu", [".menu", "menu", "*menu"],
     "# selects an id, . selects a class and a bare name selects a tag."),
    ("HTML & CSS", "basic", "Which CSS unit is relative to the width of the viewport?", "vw", ["px", "pt", "cm"],
     "1vw is 1% of the viewport width, so it scales with the browser window."),
    ("HTML & CSS", "advanced", "What does box-sizing: border-box do?", "Counts padding and border inside the element's width", ["Removes the border", "Adds extra margin outside the box", "Makes the corners round"],
     "With border-box a width of 200px stays 200px even after padding and border are added."),
    ("HTML & CSS", "basic", "Which attribute gives an image alternative text for screen readers?", "alt", ["title", "src", "caption"],
     "alt is read aloud by screen readers and shown if the image fails to load."),
    ("HTML & CSS", "advanced", "Which media query applies styles on screens narrower than 600px?", "@media (max-width: 600px)", ["@media (min-width: 600px)", "@screen (small)", "@responsive 600px"],
     "max-width matches every screen up to that width. It is the usual way to style phones."),
    ("HTML & CSS", "advanced", "Which CSS property controls the stacking order of positioned elements?", "z-index", ["order", "layer", "stack"],
     "A higher z-index sits on top of a lower one when elements overlap."),
    ("HTML & CSS", "basic", "What is semantic HTML?", "Using elements that describe their meaning, like header and article", ["Using only div tags", "Writing every tag in lowercase", "Adding inline styles everywhere"],
     "Semantic tags help search engines, screen readers and other developers understand the page."),

    # ---------------- SQL & Databases ----------------
    ("SQL & Databases", "basic", "What does SQL stand for?", "Structured Query Language", ["Simple Query Logic", "Sequential Query List", "Standard Quick Language"],
     "SQL is used to create, read, update and delete data in relational databases."),
    ("SQL & Databases", "basic", "Which SQL clause filters rows?", "WHERE", ["ORDER BY", "GROUP BY", "LIMIT"],
     "WHERE keeps only the rows that match the condition."),
    ("SQL & Databases", "basic", "Which constraint uniquely identifies each row in a table?", "PRIMARY KEY", ["FOREIGN KEY", "CHECK", "DEFAULT"],
     "A primary key is unique and cannot be empty. A foreign key points to another table's key."),
    ("SQL & Databases", "basic", "Which JOIN returns only the rows that match in both tables?", "INNER JOIN", ["LEFT JOIN", "FULL JOIN", "CROSS JOIN"],
     "INNER JOIN drops rows that have no partner. LEFT JOIN keeps every row from the left table."),
    ("SQL & Databases", "basic", "What does GROUP BY do?", "Groups rows with the same value so aggregates like COUNT can be used", ["Sorts the rows", "Deletes duplicate rows", "Renames the columns"],
     "SELECT city, COUNT(*) ... GROUP BY city counts the rows for each city."),
    ("SQL & Databases", "advanced", "What is a database index used for?", "Making lookups on a column faster", ["Encrypting the data", "Backing up the table", "Joining tables automatically"],
     "An index works like a book's index. It speeds up reads but adds a little cost to writes."),
    ("SQL & Databases", "advanced", "What is SQL injection?", "Input crafted to change the SQL query that runs", ["A very slow query", "A bug in a JOIN", "A type of index"],
     "If user text is pasted into a query, an attacker can add their own SQL to it."),
    ("SQL & Databases", "advanced", "What is the correct way to prevent SQL injection?", "Use parameterised queries or an ORM", ["Hide the table names", "Use longer passwords", "Convert all input to lowercase"],
     "Parameters keep user data separate from the SQL text, so it can never run as code."),
    ("SQL & Databases", "advanced", "What does the A in ACID stand for?", "Atomicity", ["Availability", "Accuracy", "Aggregation"],
     "Atomicity means a transaction happens completely or not at all."),
    ("SQL & Databases", "basic", "What does an ORM such as SQLAlchemy do?", "Maps Python classes to database tables", ["Compiles Python to C", "Hosts a database server", "Minifies CSS files"],
     "With an ORM you work with Python objects and it writes the SQL for you."),

    # ---------------- Git & Web ----------------
    ("Git & Web", "basic", "Which Git command saves staged changes to the repository history?", "git commit", ["git push", "git add", "git clone"],
     "git commit records a snapshot. git push only uploads commits to a remote."),
    ("Git & Web", "basic", "Which command copies a remote repository to your computer?", "git clone", ["git init", "git merge", "git stash"],
     "git clone downloads the full repository and its history."),
    ("Git & Web", "basic", "What does 'git branch feature' do?", "Creates a new branch named feature", ["Deletes the feature branch", "Merges feature into main", "Pushes feature to the server"],
     "A branch lets you work on a change without touching the main code."),
    ("Git & Web", "advanced", "What does HTTP status code 201 mean?", "Created", ["OK", "No Content", "Accepted"],
     "201 is returned when a request successfully created a new resource."),
    ("Git & Web", "basic", "What does REST stand for?", "Representational State Transfer", ["Remote Server Transfer", "Resource State Table", "Reliable Secure Transport"],
     "REST is an architectural style for web APIs built around resources and HTTP methods."),
    ("Git & Web", "advanced", "What does CORS control?", "Which other websites may call your API from a browser", ["Which users can access the database", "How CSS files are loaded", "How passwords are hashed"],
     "Browsers block cross-origin requests unless the server allows them with CORS headers."),
    ("Git & Web", "basic", "What is JSON?", "A text format for exchanging structured data", ["A database engine", "A programming language", "An image format"],
     "JSON stores data as key-value pairs and lists. Almost every web API uses it."),
    ("Git & Web", "basic", "What is a .gitignore file for?", "Telling Git which files not to track", ["Listing the project contributors", "Storing passwords safely", "Making commits faster"],
     "Use it for files like .env, uploads and virtual environments that should not be in the repository."),
    ("Git & Web", "basic", "What does HTTPS add compared with HTTP?", "Encrypts the traffic using TLS", ["Makes pages load faster", "Caches pages in the browser", "Compresses images"],
     "TLS encryption stops other people on the network from reading or changing the data."),
    ("Git & Web", "advanced", "Which HTTP method is normally used to submit a form that creates a record?", "POST", ["GET", "HEAD", "TRACE"],
     "POST sends data in the request body to create a resource. GET is for reading."),

    # ---------------- DSA & CS ----------------
    ("DSA & CS", "basic", "What is the time complexity of binary search on a sorted array?", "O(log n)", ["O(n)", "O(n log n)", "O(1)"],
     "Binary search halves the search space at every step."),
    ("DSA & CS", "basic", "Which data structure follows Last-In-First-Out (LIFO)?", "Stack", ["Queue", "Array", "Heap"],
     "Like a pile of plates, the last item you add is the first one you take off."),
    ("DSA & CS", "basic", "Which data structure follows First-In-First-Out (FIFO)?", "Queue", ["Stack", "Tree", "Set"],
     "Like a line at a ticket counter, the first person in is the first one served."),
    ("DSA & CS", "advanced", "What is the average time to look up a key in a hash table?", "O(1)", ["O(n)", "O(log n)", "O(n squared)"],
     "A hash function jumps straight to the slot, so lookup time does not grow with size."),
    ("DSA & CS", "advanced", "What is the worst-case time complexity of bubble sort?", "O(n squared)", ["O(n)", "O(log n)", "O(n log n)"],
     "Bubble sort compares neighbours in nested loops, so the work grows with n times n."),
    ("DSA & CS", "basic", "What is recursion?", "A function calling itself on a smaller problem until a base case", ["A loop that never ends", "Running code on several threads", "A step done by the compiler"],
     "Every recursive function needs a base case, otherwise it never stops."),
    ("DSA & CS", "advanced", "Which tree traversal visits left child, then root, then right child?", "Inorder", ["Preorder", "Postorder", "Level-order"],
     "Inorder traversal of a binary search tree gives the values in sorted order."),
    ("DSA & CS", "basic", "What is Big-O notation used for?", "Describing how time or memory grows as the input grows", ["Measuring exact seconds a program takes", "Checking code style", "Counting lines of code"],
     "Big-O ignores small details and shows the growth trend, such as O(n) or O(n squared)."),
    ("DSA & CS", "advanced", "Which data structure does breadth-first search use?", "Queue", ["Stack", "Heap", "Set"],
     "BFS visits nodes level by level, and a queue keeps them in that order."),
    ("DSA & CS", "advanced", "What is the difference between a process and a thread?", "A process has its own memory, threads in one process share memory", ["Threads have their own memory, processes share it", "They are the same thing", "A thread is a kind of file"],
     "Because threads share memory they are lighter, but they need care to avoid conflicts."),
]


def _build():
    questions = []
    for i, (cat, level, text, right, wrong, why) in enumerate(_ROWS):
        position = i % 4                       # 0..3 -> A..D, repeating
        options = list(wrong)
        options.insert(position, right)
        questions.append({"id": i + 1, "category": cat, "level": level,
                          "question": text, "options": options,
                          "correct_index": position, "explanation": why})
    return questions


QUESTIONS = _build()
QUESTION_BY_ID = {q["id"]: q for q in QUESTIONS}
