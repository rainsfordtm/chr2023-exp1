# Script to evaluate the performance of the parser/model combinations for
# Rainsford/Regault (2023) poster

# Create a function to calculate precision and recall from "correct"
# "missed" and "total" values
# If ncorrect, nmissed and ntotal contain multiple values, the function will SUM
# the values to give an overall score

library(ggplot2)
library(gridExtra)

get.precision.recall <- function(ncorrect, nmissed, ntotal) {
  precision = sum(ncorrect) / sum(ntotal)
  recall = sum(ncorrect) / (sum(ncorrect) + sum(nmissed))
  return(list(precision, recall))
}

# Global variable giving the key prefixes for the phenomena we wish to evaluate
PHENOMENA <- c("obj_acc_parser", "loc_parser", "en_clitic_parser", "reflexive_parser")

# Step 1. Load the csv data
summary(df <- read.csv(
  file="eval-table.csv",
  stringsAsFactors=TRUE,
  header=TRUE,
  encoding="utf-8"
))

# Step 2. Build a new df by cross-tabulating parser.mode, lemma and PHENOMENA
pr <- expand.grid(c("precision", "recall"), levels(df$parser.model), levels(df$lemma), PHENOMENA)

# Step 3. Iterate through the new table calculating precision and recall values
# for each verb
values <- c()
for (i in seq(1, nrow(pr), by=2)) {
  qwe <- subset(df, df$parser.model == pr[i,2] & df$lemma == pr[i,3])
  x <- get.precision.recall(
    ncorrect=qwe[qwe$key == paste0(pr[i,4], "_correct"),]$n,
    nmissed=qwe[qwe$key == paste0(pr[i,4], "_missed"),]$n,
    ntotal=qwe[qwe$key == paste0(pr[i,4], "_total"),]$n
  )
  values <- c(values, x[[1]], x[[2]])
}

pr <- cbind(pr, values)
colnames(pr) <- c("stat", "parser.model", "lemma", "phenomenon", "value")

# Step 4. Generate overall scores
pr.all <- expand.grid(c("precision", "recall"), levels(df$parser.model), PHENOMENA)
values <- c()
for (i in seq(1,nrow(pr.all), by=2)) {
  qwe <- subset(df, df$parser.model == pr.all[i,2])
  x <- get.precision.recall(
    ncorrect=qwe[qwe$key == paste0(pr.all[i,3], "_correct"),]$n,
    nmissed=qwe[qwe$key == paste0(pr.all[i,3], "_missed"),]$n,
    ntotal=qwe[qwe$key == paste0(pr.all[i,3], "_total"),]$n
  )
  values <- c(values, x[[1]], x[[2]])
}
pr.all <- cbind(pr.all, values)
colnames(pr.all) <- c("stat", "parser.model", "phenomenon", "value")

# Step 5. Plot the results (overall summary)

plot.precision.recall <- function(df, title) {
  qwe <- ggplot( # Set up plot
    data = df, # Data from data frame
    mapping = aes(parser.model, value, fill=stat) 
  ) +
  geom_bar(  # histogram
    stat="identity", # raw data
    position="dodge" # bars next to each other
  ) + 
  geom_text( # Add values
    aes(label=round(value, digits=4)), # use values and round to 4sf.
    position=position_dodge(width=1), # dodge like the bars
    vjust=-0.25, # move up a bit
    size=2 # make it smaller
  ) +
  ylim(0, 1) + # Scale from 0.5 to 1
  theme_minimal() + # Basic theme
  scale_x_discrete(guide = guide_axis(n.dodge=2)) + # Stop x-axis labels overlapping
  labs(title=title)
  return(qwe)
}

# Relevel to make hops-sequoia-expert first in the list
pr.all$parser.model <- relevel(pr.all$parser.model, "hops-sequoia-expert")
# Plot
x1 <- plot.precision.recall(pr.all[pr.all$phenomenon == "obj_acc_parser",], "Has direct object")
x2 <- plot.precision.recall(pr.all[pr.all$phenomenon == "loc_parser",], "Locatives")
x3 <- plot.precision.recall(pr.all[pr.all$phenomenon == "reflexive_parser",], "Reflexive")
x4 <- plot.precision.recall(pr.all[pr.all$phenomenon == "en_clitic_parser",], "Has 'en' clitic")

qwe <- grid.arrange(
  x1, x2, x3, x4,
  ncol=2,
  nrow=2
)

ggsave("figure.png", qwe, scale=2)