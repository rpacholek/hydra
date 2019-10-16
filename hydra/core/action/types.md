Action type guideline

The file types.yaml is to declare what action are possible, as well as what actions require.


normal - by default it is optional or inherited from below
!required - required field - overrides the previous one
?optional
~notAllowed
default[value] - if not given any, return value in brackets
* - any, allow not restrictive check (only required fields)
