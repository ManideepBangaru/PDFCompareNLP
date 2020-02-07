# source("Code.R")
source("dashboardTheme.R")
library(ECharts2Shiny)
if(!require(readxl)) install.packages("readxl")
library(readxl)


if(!require(shinydashboard)) install.packages("shinydashboard")
library(shinydashboard)

if(!require(shinyWidgets)) install.packages("shinyWidgets")
library(shinyWidgets)

if(!require(DT)) install.packages("DT")
library(DT)

library(shiny)
library(shinydashboard)
library(readxl)
library(data.table)
library(shinyWidgets)
setwd("D:/Accounts/ReUsableCM")

ui <- fluidPage(
  dashboardPage(
    dashboardHeader(title = "Quality Checking"),
    dashboardSidebar(
      sidebarMenu(
        menuItem("Raw Input", tabName = "rawInput"),
        menuItem("Summary", tabName = "summary"),
        menuItem("Output", tabName = "output"),br(),br(),br(),br(),br(),br(),br(),br(),br(),br(),br(),br(),br(),br(),br(),hr(),
        column(width = 12,tags$b(p("Guidelines", style = "font-size:25px")),hr(),br(),
          tags$b(p("1. Upload Pre and Post PDF in",br()," tab 'Raw Input'"),br(),
          p("2. Click on button 'Click to'",br()," Compare to compare both PDF'"),br(),
          p("3. Tab 'Summary' contains brief",br()," summary and unmatched",br()," sentences in both Pre",br()," and Post PDF.",style="word-wrap: break-word;"),br(),
          p("4. Tab Output display both Pre",br()," and Post PDF with highlighted",br()," unmatched senetences.'")),br()
        )
        ,hr()
      )
    ),
    dashboardBody(shinyDashboardThemes(
      theme = "manuallyCreated"
    ),
    tabItems(
      tabItem(tabName = "rawInput",
              fluidRow(
                box( title = "Select Pdf for Pre", status = "info",width = "6",solidHeader = T,height = "770px",
                     box(width = "12",
                         fileInput('file_input', 'upload file ( . pdf format only)', 
                                   accept = c('.pdf'),
                                   multiple = FALSE)
                     ),
                     box( title = "Pre PDF", status = "info",width = "12",solidHeader = T,
                            uiOutput("pdfview")
                     )
                ),
                box( title = "Select Pdf for Post", status = "info",width = "6",solidHeader = T,height = "770px",
                     box(width = "12",
                         fileInput('file_input1', 'upload file ( . pdf format only)', 
                                   accept = c('.pdf'),
                                   multiple = FALSE)
                     ),
                     box( title = "Post PDF", status = "info",width = "12",solidHeader = T,
                          uiOutput("pdfview1")
                     )
                ),
                column(width=12,actionButton('button', 'Click to Compare', style= 'padding-left:5%;padding-right:5%;font-size:14px;'))
              )
      ),
      tabItem(tabName = "summary",
                fluidRow(
                  box( title = "Summary", status = "info",width = "12",solidHeader = T,height = "950px",
                       box( title = "", status = "info",width = "12",
                            column(width=4,tags$b("Similarity between PDFs"),loadEChartsLibrary(),tags$div(id="test4", style="width:80%;height:350px;"),deliverChart(div_id = "test4")),
                            column(width=8,
                                column(width = 12,
                                  column(width=6,tags$b("# of Pages"),loadEChartsLibrary(),tags$div(id="test", style="width:90%;height:150px;"),
                                         deliverChart(div_id = "test")),
                                  column(width=6,tags$b("Total # of Sentences"),loadEChartsLibrary(),tags$div(id="test1", style="width:90%;height:150px;"),
                                         deliverChart(div_id = "test1"))
                                  ),
                                column(width = 12,
                                  column(width=6,tags$b("Total # of Matched Sentences"),loadEChartsLibrary(),tags$div(id="test2", style="width:90%;height:150px;"),
                                          deliverChart(div_id = "test2")),
                                  column(width=6,tags$b("Total # of Unmatched Sentences"),loadEChartsLibrary(),tags$div(id="test3", style="width:90%;height:150px;"),
                                         deliverChart(div_id = "test3"))
                                )
                            )
                       ),
                       box(title = "Differences in PDF", status = "info",width = "12",solidHeader = T,
                           box(status = "danger",title = "Unmatched Sentences in Pre PDF", width = 6,height = "350px",style = "height:310px;overflow-y: scroll;overflow-x: scroll;color:black;",
                             tableOutput("table1")
                           ),
                           box(status = "warning",title = "Unmatched Sentences in Post PDF", width = 6,height = "350px",style = "height:310px;overflow-y: scroll;overflow-x: scroll;color:black;",
                               tableOutput("table2")
                           )
                       )
                  )
                )
      ),
      tabItem(tabName = "output",
              fluidRow(
                box( title = "Processed PDF", status = "info",width = "12",solidHeader = T,height = "770px",
                     box( title = "Pre PDF", status = "info",width = "6",solidHeader = T,
                          uiOutput("pdfview2")
                     ),
                     box( title = "Post PDF", status = "info",width = "6",solidHeader = T,
                          uiOutput("pdfview3")
                     )
                )
              )
      )
    )
    )
  )
)



server <- function(input, output, session) {
  options(shiny.maxRequestSize = 50*1024^2)
  observe({
    inFile <- input$file_input
    req(input$file_input)
    tempFolder<-paste0(strsplit(input$file_input$datapath,"0.pdf")[[1]][1],inFile[[1]][1])
    print("xxxx")
    file.rename(input$file_input$datapath,paste0(tempFolder))
    print(tempFolder)
    file.copy(tempFolder,"Scripts/www", overwrite = T)
    print(inFile[[1]][1])
    tempPanel<-""
    output$pdfview <- renderUI({
        tags$iframe(style="height:500px; width:100%", src=("http://127.0.0.1:3111\\85247518_Pre_Modification.pdf"))
    })
  })
  observe({
    inFile1 <- input$file_input1
    req(input$file_input1)
    tempFolder1<-paste0(strsplit(input$file_input1$datapath,"0.pdf")[[1]][1],inFile1[[1]][1])
    file.rename(input$file_input1$datapath,paste0(tempFolder1))
    file.copy(tempFolder1,"Scripts/www", overwrite = T)
    tempPanel<-""
    output$pdfview1 <- renderUI({
      tags$iframe(style="height:500px; width:100%", src=(inFile1[[1]][1]))
    })
  })
  observeEvent(input$button,{
      
    tempFolder<-"D:\\Projects\\ReUsableCM\\Results\\"
    list_of_files <- list.files(tempFolder)
    file.copy(file.path(tempFolder,list_of_files), "Scripts/www",overwrite = T)
    #file.copy(tempFolder,"www", overwrite = T)
    output$pdfview2 <- renderUI({
      tags$iframe(style="height:620px; width:100%", src=("test3_85304012_AfterChangeDoc.pdf"))
    })
    output$pdfview3 <- renderUI({
      tags$iframe(style="height:620px; width:100%", src=("test3_85304012_BeforeChangeDoc.pdf"))
    })
    
    tempTable<-read.csv("D:\\Projects\\ReUsableCM\\Summaries\\summary_85304012.csv")
    tempTable1<-read.csv("D:\\Projects\\ReUsableCM\\Summaries\\85304012_NotMatchedData.csv")
    
    renderGauge(div_id = "test4",rate = round(tempTable[9,2],2), gauge_name = "",show.tools = FALSE,animation = TRUE)
    
    dat <- data.frame(c(tempTable[2,2]),
                      c(tempTable[1,2]))
    names(dat) <- c("DOC-B", "DOC-A")
    row.names(dat) <- c("")
    renderBarChart(div_id = "test", grid_left = '1%', direction = "vertical",
                   stack_plot = FALSE,
                   # grid_left,grid_right, grid_top, grid_bottom,
                   show.legend = TRUE, show.tools = FALSE,
                   font.size.legend = 12,
                   font.size.axis.x = 12, font.size.axis.y = 12,
                   axis.x.name = NULL, axis.y.name =NULL,
                   rotate.axis.x = 0, rotate.axis.y = 0,
                   bar.max.width = NULL,
                   animation = TRUE,
                   hyperlinks = NULL,
                   data = dat
                   )
    
    dat <- data.frame(c(tempTable[3,2]),
                      c(tempTable[4,2]))
    names(dat) <- c("DOC-B", "DOC-A")
    row.names(dat) <- c("")
    renderBarChart(div_id = "test1", grid_left = '1%', direction = "vertical",
                   stack_plot = FALSE,
                   # grid_left,grid_right, grid_top, grid_bottom,
                   show.legend = TRUE, show.tools = FALSE,
                   font.size.legend = 12,
                   font.size.axis.x = 12, font.size.axis.y = 12,
                   axis.x.name = NULL, axis.y.name = NULL,
                   rotate.axis.x = 0, rotate.axis.y = 0,
                   bar.max.width = NULL,
                   animation = TRUE,
                   hyperlinks = NULL,
                   data = dat
    )
    dat <- data.frame(c(tempTable[5,2]),
                      c(tempTable[6,2]))
    names(dat) <- c("DOC-B", "DOC-A")
    row.names(dat) <- c("")
    renderBarChart(div_id = "test2", grid_left = '1%', direction = "vertical",
                   stack_plot = FALSE,
                   # grid_left,grid_right, grid_top, grid_bottom,
                   show.legend = TRUE, show.tools = FALSE,
                   font.size.legend = 12,
                   font.size.axis.x = 12, font.size.axis.y = 12,
                   axis.x.name = NULL, axis.y.name = NULL,
                   rotate.axis.x = 0, rotate.axis.y = 0,
                   bar.max.width = NULL,
                   animation = TRUE,
                   hyperlinks = NULL,
                   data = dat
    )
    dat <- data.frame(c(tempTable[7,2]),
                      c(tempTable[8,2]))
    names(dat) <- c("DOC-B", "DOC-A")
    row.names(dat) <- c("")
    xx<-renderBarChart(div_id = "test3", grid_left = '1%', direction = "vertical",
                   stack_plot = FALSE,
                   # grid_left,grid_right, grid_top, grid_bottom,
                   show.legend = TRUE, show.tools = FALSE,
                   font.size.legend = 12,
                   font.size.axis.x = 12, font.size.axis.y = 12,
                   axis.x.name = NULL, axis.y.name = NULL,
                   rotate.axis.x = 0, rotate.axis.y = 0,
                   bar.max.width = NULL,
                   animation = TRUE,
                   hyperlinks = NULL,
                   data = dat
    )
    tempTable1<-setDT(tempTable1)
    output$table1<-renderTable({
      tempTable1[tempTable1$DocumentNo == 'A']
    })
    output$table2<-renderTable({
      tempTable1[tempTable1$DocumentNo == 'B']
    })
  })
  
  
}

shinyApp(ui, server)