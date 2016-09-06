using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Text.RegularExpressions;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            //string str3 = System.IO.Directory.GetCurrentDirectory();
            //Console.WriteLine("{0}, {1}", args[0], args[1]);
            //DirectoryInfo info = new DirectoryInfo(str3);
            //ChageName(info);
            //Console.ReadKey();
            char[] c = new char[]{'a','b', 'c','d'};
            string s = "efghi";
            System.Console.WriteLine("before: {0}", new String(c));
            System.Console.WriteLine("s length: {0}", strcpy(ref c,s));
            System.Console.WriteLine("after: {0}", new String(c));
            Console.ReadKey();

        }
        public static int strcpy( ref char[] c1, string s1)
        {
            if (c1 == null || s1 == null)
            {
                return -1;
            }
            char[] temp = new char[c1.Length * 2 + s1.Length];

            for (int i = 0; i < c1.Length; ++i)
            {
                temp[i] = c1[i];
            }
            for (int i = 0; i < s1.Length; ++i)
            {
                temp[i + c1.Length] = s1[i];
            }
            c1 = temp;
            return s1.Length;
        }
        public static void ChageName(DirectoryInfo info){
            List<string> nameList = new List<string>();
            Console.WriteLine(info.FullName);
            foreach (FileInfo f in info.GetFiles())
            {
                Regex regex = new Regex(@"\.\d\.");
                string oldName = f.FullName;
                if (regex.IsMatch(f.FullName))
                {
                    nameList.Add(f.FullName);
                }
            }

            foreach (String s in nameList)
            {
                Regex regex = new Regex(@"\.\d\.");
                string newName = regex.Replace(s, @".");
                try
                {
                    Console.WriteLine("删除文件：{0}，重命名文件：{1}", s, newName);
                    File.Move(s, newName);
                    File.Delete(s);
                }
                catch (Exception e)
                {

                }
            }

            foreach (DirectoryInfo d in info.GetDirectories())
            {
                ChageName(d);
            }
        }
    }
}
