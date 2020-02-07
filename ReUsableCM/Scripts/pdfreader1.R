library(pdftools)
# myArgs <- commandArgs(trailingOnly = TRUE)
filenameBfr <- "D:/Projects/ReUsableCM/Input_pre/85304012_Pre_Modification.pdf"
filenameAfr <- "D:/Projects/ReUsableCM/Input_post/85304012_Post_Modification.pdf"
outputName <- "D:/Projects/ReUsableCM/PDFsExtracted/"
loan <- "85304012"
num <- "1"
outputName <- paste0(outputName,loan,'_',num,'Extracted','.csv')

textBfr <- pdf_text(filenameBfr)
textAfr <- pdf_text(filenameAfr)

max.len = max(length(textBfr), length(textAfr))
textBfr = c(textBfr, rep(NA, max.len - length(textBfr)))
textAfr = c(textAfr, rep(NA, max.len - length(textAfr)))

PdfFile  = data.frame(textBfr,textAfr)
write.csv(PdfFile,outputName)