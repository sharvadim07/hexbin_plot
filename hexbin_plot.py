import argparse
import logging
import os
#import seaborn as sns
#sns.set_theme()
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(
    description='Generate Hexbin plots for table(s).')

parser.add_argument('-t', '--tables', type=str,
                    help='Table or comma seaprated tables to construct hexbin.', required=True)
parser.add_argument('-x', '--xlim', type=int,
                    help='Limit for x axis.', required=False)
parser.add_argument('-y', '--ylim', type=int,
                    help='Limit for y axis.', required=False)
parser.add_argument('-c', '--circles_tables', type=str,
                    help='Table or comma seaprated tables for add circle.', required=False)
parser.add_argument('-p', '--prefix', type=str,
                    help='prefix', required=True)

parser.add_argument('-w', '--work_dir', type=str,
                    help='Working (output) dir absolute path.', required=True)

def change_mkdir(out_dir_path):
    if not os.path.exists(out_dir_path):
        os.mkdir(out_dir_path)
    os.chdir(out_dir_path)

def plot_heat_maps(table_dict, prefix, table_circles = None, xlim = None, ylim = None):
    for i, cur_table_name in enumerate(table_dict):
        cur_table = table_dict[cur_table_name]
        x_col = 'X'
        y_col = 'Y'
        #freq_df = cur_table.groupby([x_col, y_col]).size().reset_index(name = 'Freq')                
        # Print heat map
        #pivot = freq_df.pivot(x_col, y_col, 'Freq')    
        #fig = sns.heatmap(pivot, cmap="YlGnBu", square=True)
        plt.figure(figsize=(18, 12), dpi=300)
        cmap = 'plasma'
        if (i+1)%2 == 0:
            cmap = 'inferno'
        #plt.hexbin(cur_table[x_col].values, cur_table[y_col].values,bins= 'log', cmap=cmap,mincnt = 1, gridsize = 100)
        plt.hexbin(cur_table[x_col].values, cur_table[y_col].values,bins= 'log', cmap=cmap,mincnt = 1, gridsize = 1000)
        
        # Plot a colorbar with label.
        cb = plt.colorbar()
        cb.set_label('Number of entries, log')
        if xlim != None and ylim != None:
            plt.gca().axes.set_xlim([0,xlim])
            plt.gca().axes.set_ylim([0,ylim])
        else:
            max_val = max([cur_table[x_col].values.max(), cur_table[y_col].values.max()])
            plt.gca().axes.set_xlim([0,max_val])
            plt.gca().axes.set_ylim([0,max_val])
        if isinstance(table_circles, pd.DataFrame):
            for x, y, radius in zip(table_circles['X'], table_circles['Y'], table_circles['radius']):
                plt.gca().axes.add_artist(plt.Circle((x, y), radius, color='g', lw = 3, fill=False))
        # Add title and labels to plot.
        plt.title('Hexbin of ' + cur_table_name)
        plt.xlabel('start (nucleotide position)', fontsize = 12)
        plt.ylabel('end (nucleotide position)', fontsize = 12)
        plt.savefig(prefix + '_' + cur_table_name + '.png')
        plt.close()


def read_tables(in_file_names):
    table_dict = {}
    for in_file_name in in_file_names.strip().split(','):
        table_dict[os.path.basename(in_file_name)] = pd.read_csv(in_file_name, sep='\t', names=['X', 'Y'])
    return table_dict

def read_table_circles(in_file_name):
    table_circles = pd.read_csv(in_file_name, sep='\t', names=['X', 'Y', 'radius'])
    return table_circles

def main():
    args = parser.parse_args()
    logging.basicConfig(filename=args.work_dir + '/HM_gen.log', level=logging.INFO)

    change_mkdir(args.work_dir)

    table_dict = read_tables(args.tables)
    table_circles = None
    if args.circles_tables != None:
        table_circles = read_table_circles(args.circles_tables)
        plot_heat_maps(table_dict, args.prefix, table_circles = table_circles, \
                        xlim = args.xlim, ylim = args.ylim)
    else:
        plot_heat_maps(table_dict, args.prefix, \
                        xlim = args.xlim, ylim = args.ylim)

if __name__ == "__main__":
    main()