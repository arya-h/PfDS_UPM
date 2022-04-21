import itertools
import os
import pandas as pd


def portfolio_allocation_generation():
    portfolio_allocations = itertools.combinations_with_replacement(['ST', 'CB', 'PB', 'GO', 'CA'], 5)
    # convert into list
    p_all = list(portfolio_allocations)

    # confirm that there are 126 combinations with repetition
    assert len(p_all) == 126

    # now convert it into the agreed model, ST/CB/PB/GO/CA
    formatted_portfolio_csv = []

    for el in p_all:
        # determine amount of each asset
        nST = str((el.count("ST")) * 20)
        nCB = str((el.count("CB")) * 20)
        nPB = str((el.count("PB")) * 20)
        nGO = str((el.count("GO")) * 20)
        nCA = str((el.count("CA")) * 20)

        # format to save csv file
        row = [nST, nCB, nPB, nGO, nCA]
        formatted_portfolio_csv.append(row)

    if not os.path.exists("portfolios"):
        os.mkdir("portfolios")

    df = pd.DataFrame(formatted_portfolio_csv, columns=["ST", "CB", "PB", "GO", "CA"])
    df.to_csv(f'portfolios/portfolio_allocations.csv', header=True, index=False)
    print(f'Successfully stored portfolio_allocations in the portfolios/ folder!')


if __name__ == "__main__":
    portfolio_allocation_generation()
