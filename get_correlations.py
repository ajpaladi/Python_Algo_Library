def get_correlations(usage_report):

    usage = pd.read_csv(usage_report)

    corr_dict = {'aoi_name': [], 'correlation': []}

    for i in usage['Project ID'].unique():
        vehicle = usage[(usage['Algorithms used'] == "['VEHICLE_TRAFFIC_ANALYSIS']")]
        vehicle['Project run date'] = pd.to_datetime(vehicle['Project run date'])
        vehicle = vehicle[(vehicle['Project run date'] > '2022-10-1')]
        vehicle["Project name"] = vehicle["Project name"].str.slice(stop=-7)
        vehicle.sort_values(by = "Project name", inplace = True)
        cell = usage[(usage['Algorithms used'] == "['DUDC_FOOT_TRAFFIC']")]
        cell.sort_values(by = "Project name", inplace = True)
        matched_ultra = pd.DataFrame()
        for index, row in cell.iterrows():
            matched_rows = []
            matched_df = pd.DataFrame()
            # find matching row(s) in the second dataframe based on the 'ID' column
            matching_rows = vehicle[vehicle['Project name'] == row['Project name']]
            # append matching row(s) to the corresponding list
            if not matching_rows.empty:
                matched_rows.append((matching_rows['Project ID'].iloc[0:1].values[0]))
                matched_rows.append((row['Project ID']))
                matched_df = matched_df.append((matching_rows))
                matched_df = matched_df.append((row))
                #matched_ultra = matched_ultra.append((matching_rows))
                #matched_ultra = matched_ultra.append((row))
                matched_df.to_csv('matched.csv')
                df = pd.read_csv('matched.csv')
                df.reset_index(inplace = True)
                vt = df[(df['Algorithms used'] == "['VEHICLE_TRAFFIC_ANALYSIS']")]
                ft = df[(df['Algorithms used'] == "['DUDC_FOOT_TRAFFIC']")]
                for proj in vt['Project ID']:
                    project = GoProject(proj)
                    results = project.get_foot_traffic_results()
                    vt_df = results.get_timeseries('uznorm.count', form='long')
                    vt_df['28D'] = vt_df['unique_count'].ewm(span=28).mean()
                for proj in ft['Project ID']:
                    project = GoProject(proj)
                    results = project.get_foot_traffic_results()
                    ft_df = results.get_timeseries('uznorm.count', form='long')
                    ft_df['28D'] = ft_df['unique_count'].ewm(span=28).mean()
                    aoi_name = vt_df.aoi_name.unique()
                    corr_dict['aoi_name'].append(aoi_name)
                    correlation = vt_df.corrwith(ft_df, method='spearman')
                    corr_dict['correlation'].append(correlation)
                print("Spearman Correlation Statistics for {}: {}\n".format(vt_df['aoi_name'].unique(), vt_df.corrwith(ft_df, method='spearman')))
                #vt_df.corrwith(ft_df, method='spearman')

    report = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in corr_dict.items() ]))
    return report
