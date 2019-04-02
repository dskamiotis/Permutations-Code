# Permutations-Code
This is the spreadsheet I'm working on. As you can see, the spreadsheet is in a really messy state. I have done some cleaning of the data as per the description below:

Each column heading denotes the Period/lesson in the day
each day has 7 periods/lessons- therefore monday to friday = 35 columns
each cell contains the class descriptor( the first 3 characters), the intitals of the teacher (3 characters after the "$" sign) and the room name ( which is the 3 characters after the "(" ).
I want to get teachers into groups of 3 (triads) where the following criteria is true:

At any given period/lesson in the week 2 teachers are "free" not teaching and 1 teacher is teaching.
within that very same triad in a different period there is a different teacher who is "not free" and Teaching, where the other 2 teachers are teaching
in addition in any other period the other combination of 2 teachers being "free" non teaching and the unused teacher is teaching.
See following idea for further clarification:

Initials A AND B are in the set but not C present in set ALSO C AND A in the set but not B present in set ALSO B AND C in the set but not A present in the set All 3 criteria must be true to work find the final triad

so there should be out of the thousands permutations not many combinations that fit that criteria

In simple terms, what I'm trying to find is to place teachers into groups of 3. Where 2 teachers can go into and observe the lesson of another teacher, ie, in any period, 2 teachers are free and one is teaching. You will see in each column all the teachers who are teaching at any given period and day. Therefore anyone who is not in that column we can deduce is not teaching. We want the group of 3 teachers to remain as a triad so the each get to be observed. So in any other period in the week a different teacher is teaching from the same triad and the other 2 are NOT teaching.
