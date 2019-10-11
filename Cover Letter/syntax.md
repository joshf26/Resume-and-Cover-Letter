# Cover Letter Generator Config Syntax
The config file is broken up into three parts:
- Position (information about the company/position)
- Info (information about the applicant)
- Templates (sentences/structure)

### Position and Info
The Position and Info sections contain small pieces of information about the position you are applying for and personal information. 
Fields that appear in both "Position" and "Info" sections must be formatted as lists (comma separated).
HTML is allowed, but template substitutions are only allowed in the Templates section.

### Templates
Templates are the main content of the cover letter.
Their order matters, so put them in the order you would like them to appear in the cover letter.
HTML is allowed and you can also use template substitutions.

### Template Substitutions
- Replacement (`{Key}`)
    - Replaces with the value of the associated key in either the Position or Info section.
    - If the key is present in both Position and Info sections, they must be lists and the replacement will be the intersection of the two lists.
    - For example, in the following config file, the resulting cover letter would be "Hello, my name is Josh.":
      ```ini
      [INFO]
      Name = Josh
      
      [TEMPLATE]
      Text = Hello, my name is {Name}.
      ```
    - Here is another example that evaluates to "I code in Python, C++ and JavaScript."
      ```ini
      [POSITION]
      Languages = Python, C++, Go, JavaScript
      
      [INFO]
      Languages = Python, Scala, C++, JavaScript
      
      [TEMPLATE]
      Text = I code in {Languages}.
      ```
- Conditional (`<[SkillType(Skill)]Text[SkillType(Skill)]Text...[]Text]>`)
    - Replaces with the text based on first condition that evaluates to true.
    - Conditions are surrounded by square brackets and contain two parts: the skill type, and the skill.
        - The skill type is the key that appears in both Position and Info.
        - The skill is the item to check if it is in the list for the Position.
    - If the skill is found in the list of skill type, the text next to it will be the replacement.
    - An empty condition (`[]`) is a catch-all case, which will be used as the replacement if there none of the other cases are true. 
    - For example, in the following config file, the resulting cover letter would be "I love snakes!":
      ```ini
      [POSITION]
      Languages = Python, Go
      
      [TEMPLATE]
      Text = I love <[Languages(Python)]snakes
                     [Languages(C++)]pointers
                     []programming>!
      ```
