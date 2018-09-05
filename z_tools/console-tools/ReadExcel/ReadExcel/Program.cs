using System;
using System.Collections.Generic;
using System.Data;
using System.Data.OleDb;
using System.Text;
using System.IO;

namespace ReadExcel
{
    class Program
    {

        static void ConnectOleDb(string filename)
        {
            string extend = System.IO.Path.GetExtension(filename);
            var props = new Dictionary<string, string>();
            switch (extend)
            {
                case ".xls":
                    props["Provider"] = "Microsoft.Jet.OLEDB.4.0";
                    props["Data Source"] = filename;
                    props["Extended Properties"] = "Excel 8.0";
                    break;
                default:
                    props["Provider"] = "Microsoft.ACE.OLEDB.12.0";
                    props["Extended Properties"] = "Excel 12.0";
                    break;
            }

            props["Data Source"] = filename;

            var sb = new StringBuilder();
            foreach(KeyValuePair<string, string> prop in props)
            {
                sb.Append(prop.Key);
                sb.Append('=');
                sb.Append(prop.Value);
                sb.Append(';');
            }

            Dictionary<string, List<string>> name_keys_dict = new Dictionary<string, List<string>>();
            Dictionary<string, Dictionary<string, string>> name_key_values = new Dictionary<string, Dictionary<string, string>>();
            var da = new OleDbDataAdapter();
            string sql_F = "Select * FROM [{0}]";
            string properties = sb.ToString();
            properties = properties.Substring(0, properties.Length - 1);
            using (OleDbConnection conn = new OleDbConnection(properties))
            {
                conn.Open();
                DataTable sheetnames = conn.GetOleDbSchemaTable(System.Data.OleDb.OleDbSchemaGuid.Tables, new object[] { null, null, null, "TABLE" });
                foreach (DataRow dr in sheetnames.Rows)
                {
                    string sheet_name = (string)dr["TABLE_NAME"];
                    name_key_values[sheet_name] = new Dictionary<string, string>();
                    List<string> ll = new List<string>();
                    da.SelectCommand = new OleDbCommand(String.Format(sql_F, sheet_name), conn);
                    DataSet ds = new DataSet();
                    da.Fill(ds, sheet_name);

                    DataTable dt = ds.Tables[0];
                    int start = 1;
                    int end = dt.Rows.Count;
                    for (int i = start; i < end; ++i)
                    {
                        string key = dt.Rows[i]["key"] + "";
                        string value = dt.Rows[i][1] + "";
                        if (!String.IsNullOrEmpty(key))
                        {
                            name_key_values[sheet_name][key] = value;
                            ll.Add(key);
                        }
                    }
                    name_keys_dict[sheet_name] = ll;
                }
            }


            var out_put = new Dictionary<string, List<string>>();
            foreach(var name in name_keys_dict.Keys)
            {
                List < string > reference = name_keys_dict[name];
                out_put[name] = new List<string>();

                foreach(var n in name_keys_dict.Keys)
                {
                    if (n != name)
                    {
                        List<string> search_list = name_keys_dict[n];
                        foreach(var search in search_list)
                        {
                            if (reference.Contains(search))
                            {
                                continue;
                            }
                            else
                            {
                                out_put[name].Add(search +  " " + name_key_values[n][search] + " sheet_name: " + n);
                            }
                        }
                    }
                }
            }

            if (out_put.Count != 0)
            {
                string out_put_str = "";
                using(FileStream fs = File.OpenWrite("Missing_Key.txt"))
                {
                    foreach(var name in out_put.Keys)
                    {
                        out_put_str += "=========== " + name + "start\r\n";
                        var s = out_put[name];
                        foreach(var ss in s)
                        {
                            out_put_str += ss + "\r\n";
                        }
                        out_put_str += "=========== end\r\n";
                    }
                    byte[] bytes = Encoding.UTF8.GetBytes(out_put_str.ToCharArray());
                    fs.Write( bytes,0 ,bytes.Length);
                }
            }

        }

        static void Main(string[] args)
        {
            ConnectOleDb("UI文字表待用.xlsx");
        }
    }
}
