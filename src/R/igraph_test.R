rm(list=ls())

library(igraph)


scores.df <- read.csv('~/Documents/CollegeFootball2015/data/scores.csv', header =T)

scores.df <- scores.df[, c('Winner', 'Pts', 'Loser', 'Pts.1')] 

colnames(scores.df) <- c('TEAM1', 'SCORE1', 'TEAM2', 'SCORE2')

scores.df$TEAM1 <- as.character(scores.df$TEAM1)
scores.df$TEAM2 <- as.character(scores.df$TEAM2)
scores.df$TEAM1 <- sapply(scores.df$TEAM1, function(str){ gsub('\\(.*\\) ', '', str)})

scores.df$TEAM2 <- sapply(scores.df$TEAM2, function(str){ gsub('\\(.*\\) ', '', str)})

teams.df <- read.csv('/home/jliu/Work/CollegeFootball2015/teams.csv', header = F)
colnames(teams.df) <- c('No', 'TEAM')

scores.df <- merge(scores.df, teams.df, by.x = 'TEAM1', by.y = 'TEAM')
colnames(scores.df)[colnames(scores.df) == 'No'] <- 'No1'
scores.df <- merge(scores.df, teams.df, by.x = 'TEAM2', by.y = 'TEAM')
colnames(scores.df)[colnames(scores.df) == 'No'] <- 'No2'

colnames(scores.df)[colnames(scores.df) == 'PTS.x'] <- 'PTS1'
colnames(scores.df)[colnames(scores.df) == 'PTS.y'] <- 'PTS2'


VID <- teams.df$No
NAME <- teams.df$TEAM

nodes.df <- data.frame(VID, NAME)
scores.df <- scores.df[ !is.na(scores.df$SCORE1) & !is.na(scores.df$SCORE2), ]
# if team1 is beaten by team2, then team1 -> team2
#EID <- rownames(scores.df)
# from <- ifelse(scores.df$SCORE1 > scores.df$SCORE2, scores.df$No2, score.df$No1)
# to <- ifelse(scores.df$SCORE1 > scores.df$SCORE2, scores.df$No1, score.df$No2 )

from <- scores.df$No2
to <- scores.df$No1
# EL <- rep('beaten_by', nrow(scores.df))
# 
# #DIFF <- abs(scores.df$SCORE1 - scores.df$SCORE2)*1.0
# 
# DIFF <- ifelse(scores.df$SCORE1 > scores.df$SCORE2, scores.df$PTS2, score.df$PTS1)
# 

relations <- data.frame(from, to)
g <- graph_from_data_frame(relations, directed=TRUE, vertices=nodes.df)
print(g, e=TRUE, v=TRUE)

pg <- page_rank(g, vids = V(g), directed = TRUE, damping = 0.9)

names(pg$vector)

pg.result <- data.frame(No= names(pg$vector), page_rank = pg$vector)
pg.result <- merge( pg.result, teams.df, by = 'No')

pg.result[order(-pg.result$page_rank), ][1:30,]


