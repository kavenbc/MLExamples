import os
from os.path import isfile, join
import pandas as pd

col_names = ['id','member_id','loan_amnt','funded_amnt','funded_amnt_inv','term','int_rate','installment',
             'grade','sub_grade','emp_title','emp_length','home_ownership','annual_inc','verification_status',
             'issue_d','loan_status','pymnt_plan','url','desc','purpose','title','zip_code',
             'addr_state','dti','delinq_2yrs','earliest_cr_line','fico_range_low','fico_range_high',
             'inq_last_6mths','mths_since_last_delinq','mths_since_last_record','open_acc','pub_rec','revol_bal',
             'revol_util','total_acc','initial_list_status','out_prncp','out_prncp_inv','total_pymnt',
             'total_pymnt_inv','total_rec_prncp','total_rec_int','total_rec_late_fee','recoveries',
             'collection_recovery_fee','last_pymnt_d','last_pymnt_amnt','next_pymnt_d','last_credit_pull_d',
             'last_fico_range_high','last_fico_range_low','collections_12_mths_ex_med','mths_since_last_major_derog',
             'policy_code','application_type','annual_inc_joint','dti_joint','verification_status_joint',
             'acc_now_delinq','tot_coll_amt','tot_cur_bal','open_acc_6m','open_act_il','open_il_12m',
             'open_il_24m','mths_since_rcnt_il','total_bal_il','il_util','open_rv_12m','open_rv_24m','max_bal_bc',
             'all_util','total_rev_hi_lim','inq_fi','total_cu_tl','inq_last_12m','acc_open_past_24mths',
             'avg_cur_bal','bc_open_to_buy','bc_util','chargeoff_within_12_mths','delinq_amnt',
             'mo_sin_old_il_acct','mo_sin_old_rev_tl_op','mo_sin_rcnt_rev_tl_op','mo_sin_rcnt_tl','mort_acc',
             'mths_since_recent_bc','mths_since_recent_bc_dlq','mths_since_recent_inq','mths_since_recent_revol_delinq',
             'num_accts_ever_120_pd','num_actv_bc_tl','num_actv_rev_tl','num_bc_sats','num_bc_tl','num_il_tl',
             'num_op_rev_tl','num_rev_accts','num_rev_tl_bal_gt_0','num_sats','num_tl_120dpd_2m','num_tl_30dpd',
             'num_tl_90g_dpd_24m','num_tl_op_past_12m','pct_tl_nvr_dlq','percent_bc_gt_75','pub_rec_bankruptcies',
             'tax_liens','tot_hi_cred_lim','total_bal_ex_mort','total_bc_limit','total_il_high_credit_limit',
             'revol_bal_joint','sec_app_fico_range_low','sec_app_fico_range_high','sec_app_earliest_cr_line',
             'sec_app_inq_last_6mths','sec_app_mort_acc','sec_app_open_acc','sec_app_revol_util','sec_app_open_act_il',
             'sec_app_num_rev_accts','sec_app_chargeoff_within_12_mths','sec_app_collections_12_mths_ex_med',
             'sec_app_mths_since_last_major_derog','hardship_flag','hardship_type','hardship_reason','hardship_status',
             'deferral_term','hardship_amount','hardship_start_date','hardship_end_date','payment_plan_start_date',
             'hardship_length','hardship_dpd','hardship_loan_status','orig_projected_additional_accrued_interest',
             'hardship_payoff_balance_amount','hardship_last_payment_amount','disbursement_method','debt_settlement_flag',
             'debt_settlement_flag_date','settlement_status','settlement_date','settlement_amount','settlement_percentage','settlement_term']

drop_col_name = ['member_id','grade','emp_title','pymnt_plan','desc','title','url','next_pymnt_d','policy_code',
                 'last_pymnt_d','last_pymnt_amnt','next_pymnt_d', 'last_credit_pull_d', 'funded_amnt', 'funded_amnt_inv',
                 'initial_list_status','total_pymnt','total_pymnt_inv','total_rec_late_fee','annual_inc_joint',
                 'dti_joint','revol_bal_joint','hardship_flag','hardship_type','hardship_reason','hardship_status',
                 'deferral_term','hardship_amount','hardship_start_date','hardship_end_date','payment_plan_start_date',
                 'hardship_length','hardship_dpd','hardship_loan_status','orig_projected_additional_accrued_interest',
                 'hardship_payoff_balance_amount','hardship_last_payment_amount','disbursement_method','debt_settlement_flag',
                 'debt_settlement_flag_date','settlement_status','settlement_date','settlement_amount','settlement_percentage',
                 'settlement_term']

months_dic = {"Jan" : 1, "Feb" : 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul" : 7, "Aug" : 8, "Sep": 9,
              "Oct" : 10, "Nov" : 11, "Dec" : 12}

def intstring(str) :
    iStr = 0
    for item in str:
        iStr = iStr * 62 # 2 char -capital/small + digital
        iStr = iStr + ord(item)

    return iStr


def handleYears(istr):
    if False == isinstance(istr, str):
        return 0
    istr = istr.replace(" years", "")
    if "<" in istr:
        istr = "0"
    elif "+" in istr:
        istr = "11"

    return istr


def homeownership(s):
    if "RENT" in s :
        return 1
    elif "OWN" in s :
        return 2
    elif "MORTGAGE" in s :
        return 3
    elif "OTHER" in s:
        return 4


def verificationstatus(s):
    if "Not" in s:
        return 1
    elif "Source" in s:
        return 2
    else:
        return 3


def loanstatus(s):
    if "Full" in s:
        return 1
    elif "Current" in s:
        return 2
    elif "30" in s:
        return 3
    else:
        return 4


def purpose(s):
    return len(s) + intstring(s[0:3])


def yearsmonth(s):
    if False == isinstance(s, str):
        return 0

    ss = s.split("-")

    return ss[1]+str(months_dic[ss[0]])


def yearcount(s):
    if False == isinstance(s, str):
        return 0

    ss = s.split("-")

    return int(ss[1])-1900


def appicationtype(s):
    if False == isinstance(s,str):
        return 0

    if "Individual" in s:
        return 1
    else:
        return 2


def parseCSV(file_path, filepoint):
    df = pd.read_csv(file_path,  names=col_names, skipinitialspace=True)
    irow = df.shape[0]

    #Remove space
    for col in df:
        df[col] = df[col].str.strip()

    #Delete first 2 and last 2 rows
    df = df.drop(df.index[[0,1,irow - 2, irow-1]])

    #Modify terms to month number only
    df['term'] = df['term'].str.split(' ').str[0]

    #modify rate to remove %
    df['int_rate'] = df['int_rate'].str.replace('%', '')

    #modify sub_grade with number
    df['sub_grade'] = df['sub_grade'].apply(intstring)

    #Modify emp_length with year only
    df['emp_length'] = df['emp_length'].apply(handleYears)

    #Modify Home Ownership : RENT - 0, OWN -1, MORTGAGE-2, OTHER-3
    df['home_ownership'] = df['home_ownership'].apply(homeownership)

    #Update verification: Not
    df['verification_status'] = df['verification_status'].apply(verificationstatus)

    #Update issue date
    df['issue_d'] = df['issue_d'].apply(yearsmonth)

    #Update loan status
    df['loan_status'] = df['loan_status'].apply(loanstatus)

    #Update purpose
    df['purpose'] = df['purpose'].apply(purpose)

    #Update Zipcode
    df['zip_code'] = df['zip_code'].str.replace("xx","")

    #Update addr_state
    df['addr_state'] = df['addr_state'].apply(intstring)

    #Update earliest_cr_line
    df['earliest_cr_line'] = df['earliest_cr_line'].apply(yearcount)

    #Update revol_util
    df['revol_util'] = df['revol_util'].str.replace("%","")

    #Update Annual income, dti and revol_bal to merge individual and joint
    df.annual_inc = df.annual_inc_joint.where(df.application_type == 'Joint', df.annual_inc)
    df.dti = df.dti_joint.where(df.application_type == 'Joint', df.dti)
    df.revol_bal = df.revol_bal_joint.where(df.application_type == 'Joint', df.revol_bal)

    #Update Application Type
    df['application_type'] = df['application_type'].apply(appicationtype)

    #Delete unused column
    df = df.drop(columns=drop_col_name)

    #Handle missing data Nan
    df = df.fillna(0)

    #Save to CSV file
    df.to_csv(filepoint, mode="a", index=False, header=False)
    print(irow, "done")

def joindata():
    data_path = join(os.path.dirname(os.path.realpath(__file__)), "data")
    target_file = join(os.path.dirname(os.path.realpath(__file__)), "data", "target.csv")
    for f in os.listdir(data_path):
        data_file = join(data_path,f)
        if isfile(data_file):
            parseCSV(data_file, target_file)
            print("Complete",data_file)

def dedup():
    target_file = join(os.path.dirname(os.path.realpath(__file__)), "data", "target.csv")
    filepoint = join(os.path.dirname(os.path.realpath(__file__)), "data", "targetDedup.csv")
    names = [x for x in col_names if x not in drop_col_name]
    df = pd.read_csv(target_file, names =names)

    df.drop_duplicates(subset=['id'], keep='last', inplace=True)

    df = df.drop(columns=['id'])
    df.to_csv(filepoint, mode="w", index=False, header=False)
