# sopel_modules.wordcounter
Simple word counter module for Sopel

# Installation
1. ```git clone https://github.com/Deedasmi/sopel_modules.wordcounter.git```

2. Place this folder in .sopel/modules/ (or wherever you store modules)

3. Modify ~/.sopel/default.cfg (or your sopel config file) and add the line:
```extra = ``` followed by the absolute path where you saved the module folder in step 2, including '/sopel_modules.wordcounter'

# Usage

.words *[nick] [args]*

If no nickname of arguments are provided, will list the top 5 words from all users.

# Arguments

-i Ignores words under 4 characters. Will be expanded eventually

-n *[1-9]* The number of words to grab

