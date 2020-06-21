## Requirement 

- All matches above 40% can only be considered useful.
- The code should scale up to a million properties and requirements in the system.
- All corner cases should be considered and assumptions should be mentioned
- Requirements can be without a min or a max for the budget, bedroom and a bathroom but either min or max would be surely present.
- For a property and requirement to be considered a valid match, distance should be within 10 miles, the budget is +/- 25%, bedroom and bathroom should be +/- 2.
- If the distance is within 2 miles, distance contribution for the match percentage is fully 30%
- If the budget is within min and max budget, budget contribution for the match percentage is full 30%. If min or max is not given, +/- 10% budget is a full 30% match.
- If bedroom and bathroom fall between min and max, each will contribute full 20%. If min or max is not given, match percentage varies according to the value.
- The algorithm should be reasonably fast and should be quick in responding with matches for the users once they upload their property or requirement.
###Use cases
1. Map the requirements to the properties for already existing entry and the new entry
2. Map the properties to the requirements for already existing entry and the new entry

### Approach

![](https://github.com/khingwe/radius/blob/master/Screenshot%202020-06-21%20at%2011.44.42%20PM.png)

In the above diagram shown that 1st we have find the latitude and longitude of property lies inside the square then after getting those entries filter out the 10 miles radius. 

1.	Base filter +10 miles or – 10 miles from the co-ordinate latitude and longitude get data from DB and then filter it out based on distance.

### Budget Filtering:

Two cases 
1. Max and min budgets are present
2. Max or Min any one is present

Then we find the range for 25% addition or subtraction case is added.

### Assumption:

1.	To create the latitude and longitude 10 miles if 0.16 difference is present in latitude and 0.17 difference is present in longitude
2.	Consider a normal human tendency like if within the budget bathroom and bedroom are present more then it will be fine. 


Since Bedroom and Bathroom is having low weightage so not added in the query

### Indexing 
Created a new DB prop_req_assoc table which contains prop id and req id mapping with the match percentage.

So we can filter based on query if match percentage is above 40 then will list.
