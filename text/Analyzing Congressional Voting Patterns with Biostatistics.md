# Weighted Correlation Network Analysis

# Data
I also learned some obscure facts about House Voting Rules. In the House of Representatives, territories of the United States like the Virgin Islands, DC, and Puerto Rico are represented by [[https://en.wikipedia.org/wiki/Non-voting_members_of_the_United_States_House_of_Representatives|delegates who are not allowed to cast votes]]. This fact is routinely and correctly criticized as an injustice and a hypocrisy of America's self-professed values, but the pragmatics of parliamentarianism means that it is unlikely that the existing members of the Legislature would dilute their voting power by granting statehood to the territories and full representation to their population. Furthermore, the territorial delegates almost always side with the Democratic Party, making their voting rights a partisan issue as well.

![[Pasted image 20231217222556.png]]

Knowing all this, I was confused when I realized that the non-voting Delegates (NVD) sometimes appeared in roll call votes (see above). For example, Virgin Islands delegate [Stacey Plaskett](https://en.wikipedia.org/wiki/Stacey_Plaskett) voted 0 times in 2022 until July 19th, when she suddenly [cast a vote on HR 8294](https://clerk.house.gov/Votes/2022367), a DOT and HUD appropriations bill that would die in the Senate later that month. She and the NVDs also cast votes on about a dozen other bills that July.

I was confused; how was a non-voting Delegate casting votes? Its an inherent contradiction, right?

I decided to check the [House Rules for the 117th session](https://rules.house.gov/sites/republicans.rules118.house.gov/files/117-House-Rules-Clerk-U1.pdf), and found something interesting. Rule III section 3 describes the abilities of non-voting delegates and the RC, and states that:

 > "Each Delegate and the Resident Commissioner shall be elected to serve on standing committees in the same manner as Members and shall possess in such sommittees the same powers and priveleges as the other members of the committee."
 
NVDs have the same powers within committees as any other representative. Stacey Plaskett, after all, was on the Agriculture, Budget, and Ways and Means in the 117th. They are able to cast floor votes under a very specific condition called a [Committee of the Whole House on the State of the Union](https://en.wikipedia.org/wiki/Committee_of_the_Whole_(United_States_House_of_Representatives)), when the entire House is coalesced into a single gargantuan committee.
--> continue here

# Analysis
How should we tell if two members of congress tend to vote together? There are countless binary comparison metrics, but we must remember that there are more than two possible actions to take on a bill. A member can vote yes, no, present, or be counted as not voting (typically due to health or recusal). We should not ignore 'present' votes as they can be used as protests. A recent example of this is from the Republican speaker election in early 2023 when members of the MAGA caucus repeatedly voted 'present' rather than voting for Kevin Mccarthy, whom they viewed as too moderate a Republican, or for Hakeem Jeffries, who is a Democrat. Reclassifing a present vote as a missing value to ease analysis would miss an important piece of the analysis.

What behavior should the metric value? For example, if two members vote together but against the rest of their party, should that count higher than if they voted together but alongside their leadership?

--> this means that disagreements among members with very similar 

I think that the metric should also be blind to both party and 

One issue is going to be how it weights number of votes. The problem is nancy pelosi. She's a straight democrat in voting, but as speaker of the 117th congress she barely voted. The problem with the simple overlap metric is that it artificially 

with overlap, this measures how often members lend their vote to the party...?

# Sources
Vote data was scraped from clerk.house.gov/Votes
legislator data from https://github.com/unitedstates/congress-legislators
