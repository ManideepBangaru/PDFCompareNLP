cssGradientThreeColors <- function(direction = "down", colorStart, colorMiddle, colorEnd, colorStartPos = 0,
                                   colorMiddlePos = 50, colorEndPos = 100) {
  
  ### handling direction types
  if(direction == "down"){
    colorStartSide = "top"
    colorStartSideCorner = "left top"
    colorEndSideCorner = "left bottom"
    colorDirection = "to bottom"
    
  } else if(direction == "right"){
    colorStartSide = "left"
    colorStartSideCorner = "left top"
    colorEndSideCorner = "right top"
    colorDirection = "to right"
    
  }
  
  
  ### building up css code
  cssCode <- paste0(
    # '
    #   background: ',
    colorStart, ';
    
    background: -moz-linear-gradient(
    '
    ,colorStartSide
    ,', '
    ,colorStart
    ," "
    ,colorStartPos
    ,'%, '
    ,colorMiddle
    ," ", colorMiddlePos
    ,'%,'
    ,colorEnd
    ," "
    ,colorEndPos
    ,'%
    );
    
    background: -webkit-gradient(
    '
    ,colorStartSideCorner
    ,'
    ,'
    ,colorEndSideCorner
    ,'
    ,color-stop(
    '
    ,colorStartPos
    ,'%, '
    ," "
    ,colorStart
    ,'
    )
    ,color-stop(
    '
    ,colorMiddlePos
    ,'%, '
    ,colorMiddle
    ,'
    )
    ,color-stop(
    '
    ,colorEndPos
    ,'%
    ,'
    ,colorEnd
    ,'
    )
    );
    
    background: -webkit-linear-gradient(
    '
    ,colorStartSide
    ,', '
    ," "
    ,colorStart
    ,colorStartPos
    ,'%, '
    ,colorMiddle
    ," "
    ,colorMiddlePos
    ,'%, '
    ,colorEnd
    ," "
    ,colorEndPos
    , '%
    );
    
    background: -o-linear-gradient(
    '
    ,colorStartSide
    ,', '
    , " "
    ,colorStart
    ,colorStartPos
    ,'%, '
    ,colorMiddle
    ," "
    ,colorMiddlePos
    ,'%, '
    ,colorEnd
    ," "
    ,colorEndPos
    ,'%
    );
    
    background: -ms-linear-gradient(
    '
    ,colorStartSide
    ,', '
    , " "
    ,colorStart
    ,colorStartPos
    ,'%, '
    ,colorMiddle
    ," "
    ,colorMiddlePos
    ,'%, '
    ,colorEnd
    ," "
    ,colorEndPos
    ,'%
    );
    
    background: linear-gradient(
    '
    ,colorDirection
    ,', '
    , " "
    ,colorStart
    ,colorStartPos
    ,'%, '
    ,colorMiddle
    ," "
    ,colorMiddlePos
    ,'%, '
    ,colorEnd
    ," "
    ,colorEndPos
    ,'%
    )
    '
    )
  
  ### output
  return(cssCode)
  
}

shinyDashboardThemeDIY <- function(
  appFontFamily, appFontColor, logoBackColor, bodyBackColor, headerButtonBackColor, headerButtonIconColor,
  headerButtonBackColorHover, headerButtonIconColorHover, headerBackColor, headerBoxShadowColor,
  headerBoxShadowSize, sidebarBackColor, sidebarPadding, sidebarShadowRadius, sidebarShadowColor,
  sidebarMenuBackColor, sidebarMenuPadding, sidebarMenuBorderRadius, sidebarUserTextColor, sidebarSearchBackColor,
  sidebarSearchIconColor, sidebarSearchBorderColor,  sidebarTabTextColor, sidebarTabTextSize, sidebarTabBorderStyle,
  sidebarTabBorderColor, sidebarTabBorderWidth, sidebarTabBackColorSelected, sidebarTabTextColorSelected,
  sidebarTabRadiusSelected, sidebarTabTextColorHover, sidebarTabBackColorHover, sidebarTabBorderStyleHover,
  sidebarTabBorderColorHover, sidebarTabBorderWidthHover, sidebarTabRadiusHover, boxBackColor, boxBorderRadius,
  boxShadowSize, boxShadowColor, boxTitleSize, boxDefaultColor, boxPrimaryColor, boxSuccessColor, boxWarningColor,
  boxDangerColor, tabBoxTabColor, tabBoxTabTextSize, tabBoxTabTextColor, tabBoxTabTextColorSelected, tabBoxBackColor,
  tabBoxHighlightColor, tabBoxBorderRadius, buttonBackColor, buttonTextColor, buttonBorderColor, buttonBorderRadius,
  buttonBackColorHover, buttonTextColorHover, buttonBorderColorHover, buttonHeight = 34, buttonPadding = "6px 12px",
  textboxBackColor, textboxBorderColor, textboxBorderRadius, textboxBackColorSelect, textboxBorderColorSelect,
  textboxHeight = 34, textboxPadding = "6px 12px", tableBackColor, tableBorderColor,
  tableBorderTopSize, tableBorderRowSize, primaryFontColor = "auto", successFontColor = "auto",
  warningFontColor = "auto", dangerFontColor = "auto", infoFontColor = "auto", boxInfoColor = "auto"
) {
  
  htmltools::tags$head(
    
    htmltools::tags$style(
      
      htmltools::HTML(
        
        paste0(
          
          '
          /* font: google import [OPTIONAL] */
          /* @import url("//fonts.googleapis.com/css?family=',"Roboto",'"); */
          
          /* font */
          body, label, input, button, select, box,
          .h1, .h2, .h3, .h4, .h5, h1, h2, h3, h4, h5 {
          font-family: "',appFontFamily,'";
          color: ', appFontColor, ';
          }
          
          /* font: fix for h6 */
          /* messes up sidebar user section if included above */
          .h6, h6 {
          font-family: "',appFontFamily,'";
          }
          
          /* sidebar: logo */
          .skin-blue .main-header .logo {
          background: ', logoBackColor, ';
          }
          
          /* sidebar: logo hover */
          .skin-blue .main-header .logo:hover {
          background: ', logoBackColor, ';
          }
          
          /* sidebar: collapse button  */
          .skin-blue .main-header .navbar .sidebar-toggle {
          background: ', headerButtonBackColor, ';
          color:', headerButtonIconColor, ';
          }
          
          /* sidebar: collapse button hover */
          .skin-blue .main-header .navbar .sidebar-toggle:hover {
          background: ', headerButtonBackColorHover, ';
          color:', headerButtonIconColorHover, ';
          }
          
          /* header */
          .skin-blue .main-header .navbar {
          background: ', headerBackColor, ';
          box-shadow: ', headerBoxShadowSize, ' ', headerBoxShadowColor ,';
          }
          
          /* sidebar*/
          .skin-blue .main-sidebar {
          background: ', sidebarBackColor, ';
          box-shadow: ', sidebarShadowRadius, " ", sidebarShadowColor, ';
          padding-left: ', sidebarPadding, 'px;
          padding-right: ', sidebarPadding, 'px;
          /* padding-top: 60px; */
          }
          
          /* sidebar menu */
          .main-sidebar .user-panel, .sidebar-menu, .sidebar-menu>li.header {
          white-space: nowrap;
          background: ', sidebarMenuBackColor, ';
          padding: ', sidebarMenuPadding, 'px;
          border-radius: ', sidebarMenuBorderRadius, 'px;
          }
          
          /* fix for user panel */
          .user-panel>.info>p, .skin-blue .user-panel>.info {
          color: ', sidebarUserTextColor, ';
          font-size: 12px;
          font-weight: normal;
          }
          section.sidebar .user-panel {
          padding: 10px;
          }
          
          /* sidebar: tabs */
          .skin-blue .main-sidebar .sidebar .sidebar-menu a {
          color: ', sidebarTabTextColor, ';
          font-size: ', sidebarTabTextSize ,'px;
          border-style: ', sidebarTabBorderStyle, ';
          border-color: ', sidebarTabBorderColor, ';
          border-width: ', sidebarTabBorderWidth, 'px;
          }
          
          /* sidebar: tab selected */
          .skin-blue .main-sidebar .sidebar .sidebar-menu .active a {
          color: ', sidebarTabTextColorSelected, ';
          font-size: ', sidebarTabTextSize, 'px;
          border-radius: ', sidebarTabRadiusSelected, ';
          border-style: ', sidebarTabBorderStyleHover, ';
          border-color: ', sidebarTabBorderColorHover, ';
          border-width: ', sidebarTabBorderWidthHover, 'px;
          }
          .skin-blue .sidebar-menu > li:hover > a,
          .skin-blue .sidebar-menu > li.active > a {
          color: ', sidebarTabTextColorSelected, ';
          background: ', sidebarTabBackColorSelected, ';
          border-radius: ', sidebarTabRadiusHover, ';
          }
          
          /* sidebar: tab hovered */
          .skin-blue .main-sidebar .sidebar .sidebar-menu a:hover {
          background: '
          ,sidebarTabBackColorHover, ';'
          ,'color: ', sidebarTabTextColorHover, ';
          font-size: ', sidebarTabTextSize ,'px;
          border-style: ', sidebarTabBorderStyleHover, ';
          border-color: ', sidebarTabBorderColorHover, ';
          border-width: ', sidebarTabBorderWidthHover, 'px;
          border-radius: ', sidebarTabRadiusHover, ';
          }
          
          /* sidebar: subtab */
          .skin-blue .sidebar-menu > li > .treeview-menu {
          margin: 0px;
          background: ', sidebarMenuBackColor, ';
          }
          .skin-blue .treeview-menu > li > a {
          background: ', sidebarMenuBackColor, ';
          }
          /* sidebar: subtab selected */
          .skin-blue .treeview-menu > li.active > a,
          .skin-blue .treeview-menu > li > a:hover {
          background: ', sidebarTabBackColorSelected, ';
          }
          
          /* sidebar: search text area */
          .skin-blue .sidebar-form input[type=text] {
          background: ', sidebarSearchBackColor, ';
          color: ', appFontColor, ';
          border-radius: ', textboxBorderRadius, 'px 0px 0px ', textboxBorderRadius, 'px;
          border-color: ', sidebarSearchBorderColor, ';
          border-style: solid none solid solid;
          }
          
          /* sidebar: search button */
          .skin-blue .input-group-btn > .btn {
          background: ', sidebarSearchBackColor, ';
          color: ', sidebarSearchIconColor, ';
          border-radius: 0px ', textboxBorderRadius, 'px ', textboxBorderRadius, 'px 0px;
          border-style: solid solid solid none;
          border-color: ', sidebarSearchBorderColor, ';
          }
          
          /* sidebar form */
          .skin-blue .sidebar-form {
          border-radius: 0px;
          border: 0px none rgb(255,255,255);
          margin: 10px;
          }
          
          /* body */
          .content-wrapper, .right-side {
          background: ', bodyBackColor, ';
          }
          
          /* box */
          .box {
          background: ', boxBackColor, ';
          border-radius: ', boxBorderRadius, 'px;
          box-shadow: ', boxShadowSize, ' ', boxShadowColor, ';
          }
          
          /* box: title */
          .box-header .box-title {
          font-size: ', boxTitleSize, 'px;
          }
          
          /* tabbox: title */
          .nav-tabs-custom>.nav-tabs>li.header {
          color: ', appFontColor, ';
          font-size: ', boxTitleSize, 'px;
          }
          
          /* tabbox: tab color */
          .nav-tabs-custom, .nav-tabs-custom .nav-tabs li.active:hover a, .nav-tabs-custom .nav-tabs li.active a {
          background: ', tabBoxTabColor, ';
          color: ', appFontColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          
          .nav-tabs-custom {
          box-shadow: ', boxShadowSize, ' ', boxShadowColor, ';
          }
          
          /* tabbox: active tab bg */
          .nav-tabs-custom>.nav-tabs>li.active {
          border-radius: ', tabBoxBorderRadius, 'px;
          border-top-color: ', tabBoxHighlightColor, ';
          # box-shadow: ', boxShadowSize, ' ', boxShadowColor, ';
          }
          
          /* tabbox: font color */
          .nav-tabs-custom>.nav-tabs>li.active:hover>a, .nav-tabs-custom>.nav-tabs>li.active>a {
          border-bottom-color: ', tabBoxTabColor, ';
          border-top-color: ', tabBoxHighlightColor, ';
          border-right-color: ', tabBoxHighlightColor, ';
          border-left-color: ', tabBoxHighlightColor, ';
          color: ', tabBoxTabTextColorSelected, ';
          font-size: ', tabBoxTabTextSize, 'px;
          border-radius: ', tabBoxBorderRadius, 'px;
          }
          
          /* tabbox: inactive tabs background */
          .nav-tabs-custom>.nav-tabs>li>a {
          color: ', tabBoxTabTextColor, ';
          font-size: ', tabBoxTabTextSize, 'px;
          }
          
          /* tabbox: top area back color */
          .nav-tabs-custom, .nav-tabs-custom>.tab-content, .nav-tabs-custom>.nav-tabs {
          border-bottom-color: ', tabBoxHighlightColor, ';
          background: ', tabBoxBackColor, ';
          }
          
          /* tabbox: top area rounded corners */
          .nav-tabs-custom>.nav-tabs {
          margin: 0;
          border-radius: ', tabBoxBorderRadius, 'px;
          }
          
          /* infobox */
          .info-box {
          background: ', boxBackColor, ';
          border-radius: ', boxBorderRadius, 'px;
          box-shadow: ', boxShadowSize, ' ', boxShadowColor, ';
          }
          
          /* valuebox */
          .small-box {
          border-radius: ', boxBorderRadius, 'px;
          box-shadow: ', boxShadowSize, ' ', boxShadowColor, ';
          }
          
          /* valuebox: main font color */
          .small-box h3, .small-box p {
          color: rgb(255,255,255)
          }
          
          /* box: default color */
          .box.box-solid>.box-header, .box>.box-header {
          color: ', appFontColor, ';
          }
          .box.box-solid>.box-header {
          border-radius: ', boxBorderRadius, 'px;
          }
          .box.box-solid, .box {
          border-radius: ', boxBorderRadius, 'px;
          border-top-color: ', boxDefaultColor, ';
          }
          
          /* box: info color */
          .box.box-solid.box-info>.box-header h3, .box.box-info>.box-header h3 {
          color: ', infoFontColor, ';
          }
          .box.box-solid.box-info>.box-header {
          background: ', boxInfoColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          .box.box-solid.box-info, .box.box-info {
          border-color: ', boxInfoColor, ';
          border-left-color: ', boxInfoColor, ';
          border-right-color: ', boxInfoColor, ';
          border-top-color: ', boxInfoColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          
          /* box: primary color */
          .box.box-solid.box-primary>.box-header h3, .box.box-primary>.box-header h3 {
          color: ', primaryFontColor, ';
          }
          .box.box-solid.box-primary>.box-header {
          background: ', boxPrimaryColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          .box.box-solid.box-primary, .box.box-primary {
          border-color: ', boxPrimaryColor, ';
          border-left-color: ', boxPrimaryColor, ';
          border-right-color: ', boxPrimaryColor, ';
          border-top-color: ', boxPrimaryColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          
          /* box: success color */
          .box.box-solid.box-success>.box-header h3, .box.box-success>.box-header h3 {
          color: ', successFontColor, ';
          }
          .box.box-solid.box-success>.box-header {
          background: ', boxSuccessColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          .box.box-solid.box-success, .box.box-success {
          border-color: ', boxSuccessColor, ';
          border-left-color: ', boxSuccessColor, ';
          border-right-color: ', boxSuccessColor, ';
          border-top-color: ', boxSuccessColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          
          /* box: warning color */
          .box.box-solid.box-warning>.box-header h3, .box.box-warning>.box-header h3 {
          color: ', warningFontColor, ';
          }
          .box.box-solid.box-warning>.box-header {
          background: ', boxWarningColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          .box.box-solid.box-warning, .box.box-warning {
          border-color: ', boxWarningColor, ';
          border-left-color: ', boxWarningColor, ';
          border-right-color: ', boxWarningColor, ';
          border-top-color: ', boxWarningColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          
          /* box: danger color */
          .box.box-solid.box-danger>.box-header h3, .box.box-danger>.box-header h3 {
          color: ', dangerFontColor, ';
          }
          .box.box-solid.box-danger>.box-header {
          background: ', boxDangerColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          .box.box-solid.box-danger, .box.box-danger {
          border-color: ', boxDangerColor, ';
          border-left-color: ', boxDangerColor, ';
          border-right-color: ', boxDangerColor, ';
          border-top-color: ', boxDangerColor, ';
          border-radius: ', boxBorderRadius, 'px;
          }
          
          /* button */
          .btn-default {
          background: ', buttonBackColor, ';
          color: ', buttonTextColor, ';
          border-color: ', buttonBorderColor, ';
          border-radius: ', buttonBorderRadius, 'px;
          height: ', buttonHeight, 'px;
          padding: ', buttonPadding, ';
          }
          
          /* button: hover */
          .btn-default:hover {
          background: ', buttonBackColorHover, ';
          color: ', buttonTextColorHover, ';
          border-color: ', buttonBorderColorHover, ';
          }
          
          /* button: focus */
          .btn-default:focus, .action-button:focus {
          background: ', buttonBackColor, ';
          color: ', buttonTextColor, ';
          border-color: ', buttonBorderColor, ';
          }
          
          /* button: active */
          .btn-default:active, .action-button:active {
          background: ', buttonBackColor, ';
          color: ', buttonTextColor, ';
          border-color: ', buttonBorderColor, ';
          }
          
          /* button: visited */
          .btn-default:visited {
          background: ', buttonBackColor, ';
          color: ', buttonTextColor, ';
          border-color: ', buttonBorderColor, ';
          }
          
          /* textbox */
          .form-control, .selectize-input, .selectize-control.single .selectize-input {
          background: ', textboxBackColor, ';
          color: ', appFontColor, ';
          border-color: ', textboxBorderColor, ';
          border-radius: ', textboxBorderRadius, 'px;
          height: ', textboxHeight, 'px;
          min-height: ', textboxHeight, 'px;
          padding: ', textboxPadding, ';
          }
          
          /* textbox: selected */
          .form-control:focus, .selectize-input.focus {
          color: ', appFontColor, ';
          background: ', textboxBackColorSelect, ';
          border-color: ', textboxBorderColorSelect, ';
          -webkit-box-shadow: inset 0px 0px 0px, 0px 0px 0px;
          box-shadow: inset 0px 0px 0px, 0px 0px 0px;
          }
          
          /* multi-row selectize input */
          .selectize-control.multi .selectize-input.has-items {
          height: auto;
          }
          
          /* verbatim text output */
          .qt pre, .qt code {
          font-family: ', appFontFamily, ' !important;
          }
          pre {
          color: ', appFontColor, ';
          background-color: ', textboxBackColor, ';
          border: 1px solid ', textboxBorderColor, ';
          border-radius: ', textboxBorderRadius, 'px;
          }
          
          /* drop-down menu */
          .selectize-dropdown, .selectize-dropdown.form-control {
          background: ', textboxBackColor, ';
          border-radius: 4px;
          }
          
          /* table */
          .table {
          background: ', tableBackColor, ';
          border-radius: ', textboxBorderRadius, 'px;
          }
          
          /* table: row border color*/
          .table>tbody>tr>td, .table>tbody>tr>th, .table>tfoot>tr>td, .table>tfoot>tr>th, .table>thead>tr>td, .table>thead>tr>th {
          border-top: ', tableBorderRowSize, 'px solid ', tableBorderColor, ';
          }
          
          /* table: top border color*/
          .table>thead>tr>th {
          border-bottom: ', tableBorderTopSize, 'px solid ', tableBorderColor, ';
          }
          
          /* table: hover row */
          .table-hover>tbody>tr:hover {
          background-color: ', tableBorderColor, ';
          }
          
          /* table: stripe row */
          .table-striped>tbody>tr:nth-of-type(odd) {
          background-color: ', tableBorderColor, ';
          }
          
          /* table: body colour */
          table.dataTable tbody tr {
          background-color: ', tableBackColor, ' !important;
          }
          
          /* table: footer border colour */
          table.dataTable {
          border: 0px !important;
          }
          
          /* datatable: selected row */
          table.dataTable tr.selected td, table.dataTable td.selected {
          background-color: ', boxSuccessColor, ' !important;
          color: rgb(0,0,0) !important;
          }
          
          /* datatable: hover row */
          table.dataTable tr.hover td, table.dataTable td.hover {
          background-color: ', tableBorderColor, ' !important;
          }
          table.dataTable.hover tbody tr:hover, table.dataTable.display tbody tr:hover {
          background-color: ', tableBorderColor, ' !important;
          }
          table.dataTable.row-border tbody th, table.dataTable.row-border tbody td,
          table.dataTable.display tbody th, table.dataTable.display tbody td {
          border-top: 1px solid ', tableBorderColor, ' !important;
          }
          
          /* datatable: stripe row */
          table.dataTable.stripe tbody tr.odd, table.dataTable.display tbody tr.odd {
          background-color: ', tableBorderColor, ' !important;
          }
          
          /* datatable: page control */
          .dataTables_wrapper .dataTables_paginate .paginate_button {
          color: ', appFontColor, ' !important;
          }
          
          /* datatable: table info */
          .dataTables_wrapper .dataTables_paginate .paginate_button.disabled,
          .dataTables_wrapper .dataTables_paginate .paginate_button.disabled:hover,
          .dataTables_wrapper .dataTables_paginate .paginate_button.disabled:active {
          color: ', appFontColor, ' !important;
          }
          .dataTables_wrapper .dataTables_length, .dataTables_wrapper .dataTables_filter,
          .dataTables_wrapper .dataTables_info, .dataTables_wrapper .dataTables_processing,
          .dataTables_wrapper .dataTables_paginate {
          color: ', appFontColor, ' !important;
          }
          .dataTables_wrapper .dataTables_length, .dataTables_wrapper .dataTables_filter,
          .dataTables_wrapper .dataTables_info, .dataTables_wrapper .dataTables_processing,
          .dataTables_wrapper .dataTables_paginate {
          color: ', appFontColor, ' !important;
          }
          
          /* datatable search box */
          .dataTables_wrapper .dataTables_filter input {
          background-color: ', textboxBackColor, ';
          border: 1px solid ', textboxBorderColor, ';
          border-radius: ', textboxBorderRadius, 'px;
          }
          
          /* notification and progress bar */
          .progress-bar {
          background-color: ', boxSuccessColor, ';
          }
          .shiny-notification {
          height: 80px;
          font-family: ', appFontFamily, ';
          font-size: 15px;
          color: rgb(0,0,0);
          background-color: rgb(225,225,225);
          border-color: rgb(205,205,205);
          border-radius: 10px;
          margin-left: -450px !important;
          }
          
          /* horizontal divider line */
          hr {
          border-top: 1px solid rgb(215,215,215);
          }
          
          /* modal */
          .modal-body {
          background-color: ', boxBackColor, ';
          }
          
          .modal-footer {
          background-color: ', boxBackColor, ';
          }
          
          .modal-header {
          background-color: ', boxBackColor, ';
          }
          
          '
          
        )
        
      )
      
      )
    
    )
  
}

shinyDashboardThemes <- function(theme){
    return(manually_Created)
}

### Themes ------------------------------------------------------------------
### theme_manually_Created -----------------------------------------------------
#' @export
manually_Created <- shinyDashboardThemeDIY(
  
  ### general
  appFontFamily = "Arial"
  ,appFontColor = "rgb(0,0,0)"
  ,primaryFontColor = "rgb(0,0,0)"
  ,infoFontColor = "rgb(0,0,0)"
  ,successFontColor = "rgb(0,0,0)"
  ,warningFontColor = "rgb(0,0,0)"
  ,dangerFontColor = "rgb(0,0,0)"
  ,bodyBackColor = cssGradientThreeColors(
    direction = "right"
    ,colorStart = "rgb(3,22,56)"
    ,colorMiddle = "rgb(98, 186, 208)"
    ,colorEnd = "rgb(30, 145, 174)"
    ,colorStartPos = 0
    ,colorMiddlePos = 60
    ,colorEndPos = 100
  )
  
  
  ### header
  ,logoBackColor = "rgb(23,103,124)"
  
  ,headerButtonBackColor = "rgb(37, 112, 142)"
  ,headerButtonIconColor = "rgb(75,75,75)"
  ,headerButtonBackColorHover = "rgb(210,210,210)"
  ,headerButtonIconColorHover = "rgb(0,0,0)"
  
  ,headerBackColor = "rgb(37, 112, 142)"
  ,headerBoxShadowColor = "#aaaaaa"
  ,headerBoxShadowSize = "2px 2px 2px"
  
  ### sidebar
  ,sidebarBackColor = cssGradientThreeColors(
    direction = "down"
    ,colorStart = "rgb(20,97,117)"
    ,colorMiddle = "rgb(56,161,187)"
    ,colorEnd = "rgb(3,22,56)"
    ,colorStartPos = 0
    ,colorMiddlePos = 50
    ,colorEndPos = 100
  )
  ,sidebarPadding = 0
  
  ,sidebarMenuBackColor = "transparent"
  ,sidebarMenuPadding = 0
  ,sidebarMenuBorderRadius = 0
  
  ,sidebarShadowRadius = "3px 5px 5px"
  ,sidebarShadowColor = "#aaaaaa"
  
  ,sidebarUserTextColor = "rgb(255,255,255)"
  
  ,sidebarSearchBackColor = "rgb(55,72,80)"
  ,sidebarSearchIconColor = "rgb(255,255,255)"
  ,sidebarSearchBorderColor = "rgb(55,72,80)"
  
  ,sidebarTabTextColor = "rgb(255,255,255)"
  ,sidebarTabTextSize = 13
  ,sidebarTabBorderStyle = "none none solid none"
  ,sidebarTabBorderColor = "rgb(35,106,135)"
  ,sidebarTabBorderWidth = 1
  
  ,sidebarTabBackColorSelected = cssGradientThreeColors(
    direction = "right"
    ,colorStart = "rgba(153, 153, 153,1)"
    ,colorMiddle = "rgba(242, 242, 242,1)"
    ,colorEnd = "rgba(128, 128, 128,1)"
    ,colorStartPos = 0
    ,colorMiddlePos = 30
    ,colorEndPos = 100
  )
  ,sidebarTabTextColorSelected = "rgb(0,0,0)"
  ,sidebarTabRadiusSelected = "0px 20px 20px 0px"
  
  ,sidebarTabBackColorHover = cssGradientThreeColors(
    direction = "right"
    ,colorStart = "rgba(89, 89, 89,1)"
    ,colorMiddle = "rgba(38, 38, 38,1)"
    ,colorEnd = "rgba(166, 166, 166,1)"
    ,colorStartPos = 0
    ,colorMiddlePos = 30
    ,colorEndPos = 100
  )
  ,sidebarTabTextColorHover = "rgb(242, 242, 242)"
  ,sidebarTabBorderStyleHover = "none none solid none"
  ,sidebarTabBorderColorHover = "rgb(75,126,151)"
  ,sidebarTabBorderWidthHover = 1
  ,sidebarTabRadiusHover = "0px 20px 20px 0px"
  
  ### boxes
  ,boxBackColor = "rgb(255,255,255)"
  ,boxBorderRadius = 5
  ,boxShadowSize = "0px 1px 1px"
  ,boxShadowColor = "rgba(0,0,0,.1)"
  ,boxTitleSize = 16
  ,boxDefaultColor = "rgb(210,214,220)"
  ,boxPrimaryColor = "rgba(44,222,235,1)"
  ,boxInfoColor = "rgb(210,214,220)"
  ,boxSuccessColor = "rgba(10, 110, 117,1)"
  ,boxWarningColor = cssGradientThreeColors(
    direction = "right"
    ,colorStart = "rgb(204, 238, 255)"
    ,colorMiddle = "rgb(217, 217, 217)"
    ,colorEnd = "rgb(255,255,255)"
    ,colorStartPos = 0
    ,colorMiddlePos = 60
    ,colorEndPos = 100
  )
  ,boxDangerColor = cssGradientThreeColors(
    direction = "right"
    ,colorStart = "rgb(204, 255, 238)"
    ,colorMiddle = "rgb(217, 217, 217)"
    ,colorEnd = "rgb(255,255,255)"
    ,colorStartPos = 0
    ,colorMiddlePos = 60
    ,colorEndPos = 100
  )
  
  ,tabBoxTabColor = "rgb(255,255,255)"
  ,tabBoxTabTextSize = 14
  ,tabBoxTabTextColor = "rgb(0,0,0)"
  ,tabBoxTabTextColorSelected = "rgb(0,0,0)"
  ,tabBoxBackColor = "rgb(255,255,255)"
  ,tabBoxHighlightColor = "rgba(44,222,235,1)"
  ,tabBoxBorderRadius = 5
  
  ### inputs
  ,buttonBackColor = cssGradientThreeColors(
    direction = "down"
    ,colorStart = "rgb(20,97,117)"
    ,colorMiddle = "rgb(56,161,187)"
    ,colorEnd = "rgb(3,22,56)"
    ,colorStartPos = 0
    ,colorMiddlePos = 40
    ,colorEndPos = 100
  )
  ,buttonTextColor = "rgb(255,255,255)"
  ,buttonBorderColor = "rgb(200,200,200)"
  ,buttonBorderRadius = 5
  
  ,buttonBackColorHover =cssGradientThreeColors(
    direction = "right"
    ,colorStart = "rgb(20,97,117)"
    ,colorMiddle = "rgb(56,161,187)"
    ,colorEnd = "rgb(3,22,56)"
    ,colorStartPos = 0
    ,colorMiddlePos = 40
    ,colorEndPos = 100
  )
  ,buttonTextColorHover = "rgb(255,255,255)"
  ,buttonBorderColorHover = "rgb(200,200,200)"
  
  ,textboxBackColor = "rgb(255,255,255)"
  ,textboxBorderColor = "rgb(200,200,200)"
  ,textboxBorderRadius = 5
  ,textboxBackColorSelect = "rgb(245,245,245)"
  ,textboxBorderColorSelect = "rgb(200,200,200)"
  
  ### tables
  ,tableBackColor = "rgb(255,255,255)"
  ,tableBorderColor = "rgb(210,214,220)"
  ,tableBorderTopSize = 1
  ,tableBorderRowSize = 1
)
