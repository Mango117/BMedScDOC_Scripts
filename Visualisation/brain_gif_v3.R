#Working, and saves gif file to location. Need to search up locatino in finder with Cmd+Shift+G

setwd("/Users/manojarachige/Documents/Coding/BmedScDOC1/BMedScDOC_Scripts/Visualisation")
library(rgl)
library(misc3d)
library(MNITemplate)
library(aal)
library(neurobase)
library(magick)
library(dplyr)

img = aal_image()
template = readMNI(res = "2mm")
cut <- 4500
dtemp <- dim(template)

# All of the sections you can label from aal atlas
labs = aal_get_labels()


#set up table: 2 rows [brain area] and [number of mentions]
df <- read.csv(file = "/Users/manojarachige/Documents/Coding/BmedScDOC1/Assets/displaygiftest.csv", header = FALSE)
df <- df[c(1:2), ]
df <- t(df)
df <- df[-1, ]

#cleanup
df <- as_tibble(df)
df <- rename(df, Number = 2)
df <- rename(df, Area = 1)
df$Number <- as.numeric(as.character(df$Number))
df <- df[order(df$Number),]

#Get colfunc 
colfunc <- colorRampPalette(c("lightblue", "red"))
y <- nrow(df)
colfunc(y)
plot(rep(1,y),col=colfunc(y),pch=19,cex=3)

#add colfunc to df as a new column
df <- cbind(df,colfunc(y))


#contour for MNI template
contour3d(template, x=1:dtemp[1], y=1:dtemp[2], z=1:dtemp[3], level = cut, alpha = 0.1, draw = TRUE)


#iterate over dataframe
for (row in 1:nrow(df)){
  area = labs$index[grep(df[row,1], labs$name)]
  mask = remake_img(vec = img %in% area, img = img)
  contour3d(mask, level = c(0.5), alpha = c(0.5), add = TRUE, color=c(df[row,3]) )
}


#MOVIE CREATE
### add text
text3d(x=dtemp[1]/2, y=dtemp[2]/2, z = dtemp[3]*0.98, text="Top")
text3d(x=-0.98, y=dtemp[2]/2, z = dtemp[3]/2, text="Right")
#create movie
movie3d(spin3d(),duration=12, fps = 5, startTime = 0, movie = "movie", convert = TRUE, type = "gif", top = TRUE)

