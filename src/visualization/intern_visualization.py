import matplotlib.pyplot as plt
import pandas as pd

colors: list = ['yellow', 'orange', 'blue', 'green', 'red', 'purple', 'pink']

def ages_linear_data_interpolation(df1: pd.DataFrame, df2: pd.DataFrame, title: str, show_fig=False) -> str:
        plt.figure(figsize=(16, 8))
        for i, column in enumerate(df1.columns):
            plt.plot(df1[column], label=f'Original: {column}', linestyle='dotted', linewidth=6, color=colors[i % len(colors)])
            plt.plot(df2[column], label=f'Interpol. Linear: {column}', linestyle='solid', linewidth=2, color=colors[i % len(colors)])
        
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small')
        plt.xlabel('Index')
        plt.ylabel('Age (Ma)')
        plt.title(title)
        plt.subplots_adjust(right=0.75)
        plt.tight_layout()  # Ajusta o layout para garantir que tudo caiba
        plt.grid(True)
        if show_fig:
            plt.show()
        plt.savefig(f"report/figures/{title}.png")
        return f"report/figures/{title}.png"

