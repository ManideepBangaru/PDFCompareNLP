library(pdftools)
# myArgs <- commandArgs(trailingOnly = TRUE)
filenameBfr <- args[1]
filenameAfr <- args[2]
outputName <- args[3]
loan <- args[4]
num <- args[5]
outputName <- paste0(outputName,loan,'_',num,'Extracted','.csv')

textBfr <- pdf_text(filenameBfr)
textAfr <- pdf_text(filenameAfr)

max.len = max(length(textBfr), length(textAfr))
textBfr = c(textBfr, rep(NA, max.len - length(textBfr)))
textAfr = c(textAfr, rep(NA, max.len - length(textAfr)))

PdfFile  = data.frame(textBfr,textAfr)
write.csv(PdfFile,outputName)