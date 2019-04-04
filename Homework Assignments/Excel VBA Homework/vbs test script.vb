Sub StockTesting()

   ' Set an initial variable for holding the stock ticker
   Dim Ticker As String

   ' Set an initial variable for holding the total volume per stock ticker
   Dim Ticker_Total_Volume As Long

   ' Set an initial variable for holding the opening and closing price per stock ticker
   Dim Open_Price As Double
   Dim Close_Price As Double

   ' Set an initial variable for annual change in stock price
   Dim Yearly_Change As Double
   Dim Percent_Change As Double

   ' Keep track of the location for each stock ticker in the summary table
   Dim Summary_Table_Row As Integer

   ' Create variables to track the last row and column in the data
   Dim Last_Row As Long
   Dim Last_Column As Integer

   Dim ws As Worksheet

   For Each ws In Worksheets

       Summary_Table_Row = 2
       Ticker_Total_Volume = 0
       Last_Row = ws.Cells(Rows.Count, 1).End(xlUp).Row
       Last_Column = ws.Cells(1, Columns.Count).End(xlToLeft).Column

       ' Loop through all stock data
       For i = 2 To Last_Row

           ' Check if we are still within the same stock ticker, if it is not...
           If ws.Cells(i - 1, 1).Value <> ws.Cells(i, 1).Value And ws.Cells(i, 3) <> 0 Then

               ' Need to find first non-zero starting value

               ElseIf ws.Cells(i, 3).Value = 0 Then Open_Price = 0.1

               ElseIf ws.Cells(i + 1, 1).Value <> ws.Cells(i, 1).Value Then

               ' Set the ticker name
               Ticker = ws.Cells(i, 1).Value

               ' Set Close Price
               Close_Price = ws.Cells(i, 6).Value

               ' Calc Yearly Change
               Yearly_Change = Close_Price - Open_Price

               'Calc Percent Change
               Percent_Change = ((Yearly_Change / Open_Price) - 1)

               ' Add to the Volume Total
               Volume_Total = Volume_Total + ws.Cells(i, 7).Value

               ' Print the stock Ticker in the Summary Table
               ws.Range("I" & Summary_Table_Row).Value = Ticker

               ' Print the Yearly Change in the Summary Table
               ws.Range("J" & Summary_Table_Row).Value = Yearly_Change

               ' Print the Percent Change in the Summary Table
               ws.Range("K" & Summary_Table_Row).Value = Percent_Change

               ' Print the stock Volume in the Summary Table
               ws.Range("L" & Summary_Table_Row).Value = Volume_Total

               ' Add one to the summary table row
               Summary_Table_Row = Summary_Table_Row + 1

               ' Reset the Volume Total
               Volume_Total = 0

               'Reset the Yearly Change
               Yearly_Change = 0

               ' Reset the Percent Change
               Percent_Change = 0

           ' If the cell immediately following a row is the same ticker...
           Else

           ' Add to the Volume Total
           Volume_Total = Volume_Total + ws.Cells(i, 7).Value

       End If

   Next i

Next ws

End Sub