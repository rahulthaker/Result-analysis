import base64
def report_downlaoder(fc,sc,pc,tp,fig):
    with open("report.html", 'w') as f:
        f.write(
            'First-class' + fc.to_html() + '\n\nSecond class' + sc.to_html() + '\n\npass class' + pc.to_html() + '\n\ntoppers' +tp.to_html() + '\nPassing chart' +fig.to_html()
        )
    with open('report.html', 'rb') as f:
        html_file = f.read()

    bin_str = base64.b64encode(html_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="report.html">Download Report</a>'
    return href