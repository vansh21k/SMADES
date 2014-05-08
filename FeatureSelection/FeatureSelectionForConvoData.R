#Feature Selection script in R

data = read.table(file = "train_0.csv", head = TRUE, sep = "," )
data = as.data.frame.matrix(data)
drops = c("SOURCE_IP","DEST_IP","SOURCE_PORT","DEST_PORT","TIMESTAMP", "FIRST_PACKET_SIZE", "MAX_PACKET_SIZE")
data = data[,!(names(data) %in% drops)]
df = data
## Best first Search based
library(FSelector)
library(rpart)
library(mlbench)
evaluator <- function(subset) {
#k-fold cross validation
k <- 5
splits <- runif(nrow(df))
results = sapply(1:k, function(i) {
test.idx <- (splits >= (i - 1) / k) & (splits < i / k)
train.idx <- !test.idx
test <- df[test.idx, , drop=FALSE]
train <- df[train.idx, , drop=FALSE]
tree <- rpart(as.simple.formula(subset, "LABEL"), train)
error.rate = sum(test$LABEL != predict(tree, test, type="c")) / nrow(test)
return(1 - error.rate)
})
print(subset)
print(mean(results))
return(mean(results))
}
#subset <- best.first.search(names(df)[-75], evaluator)
#f <- as.simple.formula(subset, "LABEL")
#print(f)

## CFS based
#subset <- cfs(LABEL~., df)
#f <- as.simple.formula(subset, "LABEL")
#print(f)

##Random forest based importance measure
library(mlbench)
weights <- random.forest.importance(LABEL~., df, importance.type = 1)
print(weights)

#Cutoff function may cause an error - weka dependencies
subset <- cutoff.k(weights, 5)
f <- as.simple.formula(subset, "LABEL")
print(f)


