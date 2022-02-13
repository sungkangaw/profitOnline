from cx_Freeze import setup, Executable

build_exe_options = {"excludes": ["tkinter", "sqlite3",
                                  "scipy.lib.lapack.flapack",
                                  "PyQt4.QtNetwork",
                                  "PyQt4.QtScript",
                                  "numpy.core._dotblas",
                                  "numpy.polynomial",
                                  "numpy.matrixlib",
                                  "numpy.random",
                                  "pandas",
                                  "multiprocessing",
                                  "email",
                                  "html",
                                  "http",
                                  "asyncio",
                                  "unittest"
                                  "PyQt5"],
                     "optimize": 2}

setup(name = "calculate" ,
      version = "0.2.9" ,
      description = "" ,
      options = {"build_exe": build_exe_options},
      executables = [Executable("calculate.py")])

#To package:
#python setup.py build

#0.2.4
#Add filter Lazada for excluding Orders-Claims, Refunds, Refunds-Lazada Fees, Refunds-Claims
#Add build options to exclude unused package

#0.2.5
#Change shopee SERVICE_FEE column from 35 to 36

#0.2.6
#Add service_fee (column 16) to shopee output file

#0.2.7
#Shopee
#change service fee to col 37
#change province to col 45
#change district to col 46
#add ' in front of tracking no
#Lazada
#add bonus column - change net profit formula
#add filtered transaction type - REFUND_MARKETING_FEES, OTHER_SERVICES, SPONSERED_DISCOVERY
#add Orders-Marketing Fees as service fee

#0.2.8
#Fix shopee bonus column (not used)

#0.2.9
#Seperate columns into config file