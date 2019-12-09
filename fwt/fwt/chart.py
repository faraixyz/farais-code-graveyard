from pygal import Line

def make_chart(values, seulav):
    chart = Line(title="It Works!")
    chart.add("Weight (lbs)", values)
    chart.add("Weight Trend", seulav)
    chart.render_to_file('fwt/static/img/todate.svg')   
    
    return chart
