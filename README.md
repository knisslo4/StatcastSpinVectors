# Statcast 2D pitch data --> Hawkeye 3D spin vectors
Big task here!

## Background
Statcast's pitch data is derived from Hawkeye's 3D pitch data but only showcases 2D information. This is a problem when working on machines like the Trajekt pitching machine like I was fortunate enough to be able to do. Trajket's input is pitch spin vector information
like SpinX, SpinY, and SpinZ, as well as other metrics like Seam Orientation, Release Position, and Pitch Velocity. The only people who have access to this data are MLB orgs so in an effort to overcome this hurdle I spent countless hours learning the physics of a baseball
and spin vectors to get pretty close to the actual values.

## Problems
There are problems w/ this model though because it's so variable pitcher by pitcher. Also, originally I had not converted degrees to radians and still haven't so this code will not output a good value until that's done.

## Next Steps
Using this data we can theoretically throw up any pitcher who's ever had statcast data and throw their arsenal. This becomes extremely important when trainers are preparing hitters to face opposing pitchers as well as when explaining a new pitch to a pitcher. They can
physically see how the pitch moves and tweak things here and there to make it unhittable. This also becomes important when scouting for players and targeting key players to acquire that others may pass on. With this data we can play around with different adjusts and see
if there's a diamond in the rough of a players aresenal by modifying just a few things.

### HUGE shoutout to Prof. Alan Nathan for his expertise on a project like this!!!
