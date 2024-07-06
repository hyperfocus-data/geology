"""
Caio Madeira

"""


from src.visualization.intern_visualization import ages_linear_data_interpolation
from src.data.analyze import eon_ages_linear, eon_ages_median, eon_ages_origin
from report.report import generate_report

lines: list = [
    ' For a accurate analytics of data validation followed the indecision of witch algori-',
    'thm to use, it was maked an plot witch shows the variation between the original data ',
    '(in untouched dataframe) with some values stayed NaN (empty) and a variation of original',
    'data that underwent a linear interpolation that filled in empty values with a "linear predi-',
    'cion" (estimation of missing data) filling by continuous data.',
    ' ',
    ' Linear interpolation was used because is the most common used techniques for unknown values',
    ' estimation witch is in between two known interval. It is a simple form of interpolation that ',
    'assumes that variation is linear.'
]

if __name__ == "__main__":
    plot1_path = ages_linear_data_interpolation(df1=eon_ages_origin.dataframe, df2=eon_ages_linear.dataframe, title='Impact of Linear Interpolation x Original data (Ages (Ma))' )
    generate_report(filename="intern_linearinterpo_original", 
                    document_title='Impact of Linear Interpolation x Original data (Ages (Ma))',
                    title='Impact of Linear Interpolation x Original data (Ages (Ma))',
                    images=[plot1_path],
                    textlines=lines)
