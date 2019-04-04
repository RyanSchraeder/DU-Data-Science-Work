Sub StockVolume()
    
    'Create for loop starting with all worksheets since ws is defined as a Worksheet
    'Nest a loop with the values of all variables, and in that loop you'll be summarizing data in columns I and J for Ticker and Volume totals
    'use a condition to put information into I, J, K, L
    'label I, J, K, L
    
    Dim ws As Worksheet
    
    For Each ws In Worksheets
    
    ' - last row in the sheet as a long type (loads of rows)
    ' - last column in the sheet (12 columns used)
    ' - worksheet currently active
    ' - total for all rows
    ' - ticker as a string value
    ' - total ticker sum for all rows
    ' - opening price of the ticker
    ' - closing price of the ticker
    ' - difference in stock price throughout the year
    ' - value of the stock throughout the year by percentage

    Dim Summary_Table_Row As Integer
    Dim VolumeTotal As Double
    
    Summary_Table_Row = 2
    VolumeTotal = 0
    
    
    Dim LastRow As Long
    Dim LastColumn As Integer
    
    
       'determine the last row
    
        LastRow = Cells(Rows.Count, 1).End(xlUp).Row
        
    'determine the last column
    
        LastColumn = ws.Cells(1, Columns.Count).End(xlToLeft).Column
        
    'ticker
    
    Dim Ticker As String
    Dim TickerVolume As Long
    
    TickerVolume = 0
    
    'stock prices
    
    Dim OpenPrice As Double
    Dim ClosePrice As Double

    
    'stock price changes
    
    Dim YearlyPriceChange As Double
    YearlyPriceChange = 0
    Dim YearlyPercentage As Double
    YearlyPercentage = 0
    
    
        For i = 2 To LastRow
    
            If ws.Cells(i - 1, 1) <> ws.Cells(i, 1).Value And ws.Cells(i, 3) <> 0 Then
                
        'Define the ticker name as string
        
                Ticker = ws.Cells(i, 1).Value
                    ws.Range("I" & Summary_Table_Row).Value = TickerVolume
                    
            ElseIf ws.Cells(i, 3).Value = 0 Then OpenPrice = 0.1
                
        'Define the ClosePrice from F2 as Integer (Double type declared due to volume of data)
        
            ElseIf ClosePrice = ws.Cells(i, 6).Value Then
                
            ElseIf YearlyPriceChange = ClosePrice - OpenPrice Then
                    ws.Range("L" & Summary_Table_Row).Value = YearlyPriceChange
                    
        'Define the Yearly Percentage of stock performance on average by dividing change in price overall by the opening price, make sure to round
        
            ElseIf YearlyPercentage = ((YearlyPriceChange / OpenPrice) - 1) Then
                    ws.Range("K" & Summary_Table_Row).Value = YearlyPercentage
                    
         'Add to the volume total
         
            ElseIf VolumeTotal = VolumeTotal + ws.Cells(i, 7).Value Then
                    ws.Range("J" & Summary_Table_Row).Value = VolumeTotal

                ws.Cells(1, 10).Value = "Volume Total"
                ws.Cells(1, 9).Value = "Ticker"
                ws.Cells(1, 11).Value = "Yearly Percentage Average"
                ws.Cells(1, 12).Value = "Yearly Price Average"
                
                Summary_Table_Row = Summary_Table_Row + 1
                
        'Reset the volume total
        
                VolumeTotal = 0
                
            Else
            
                VolumeTotal = VolumeTotal + ws.Cells(i, 7).Value
            
            End If
        
        Next i
        
    Next ws
    
End Sub



