using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp2
{
    class Program
    {

        const string FILE_ENCRYPT_TITLE = "haitong";

        const int FILE_ENCRYPT_VERSION = 1;

        const string FILE_ENCRYPT_PASSWORD = "qwer";


        static void Main(string[] args)
        {

            var file = "";
            if(args.Length >= 1)
            {
                file = args[0];
            }

            while (true)
            {
                var keyInfo = Console.ReadKey();

                if(keyInfo.Key == ConsoleKey.Escape)
                {
                    break;
                }

                var keyChar = keyInfo.KeyChar;
                if (keyChar == 'e')
                {
                    AES_EncryptFile(file);
                    Console.WriteLine("encrypt succeed \n");
                }
                else if (keyChar == 'd')
                {
                    var bytes = AES_Decrypt(File.ReadAllBytes(file));
                    File.WriteAllBytes($"{file}.decrypt", bytes);
                    Console.WriteLine("decrypt succeed \n");
                }
                else if(keyChar == 'q')
                {
                    break;
                }
                else
                {
                    Console.WriteLine("\nonly support keyboard d (decrypt) e(encrypt) q(quit)");
                }
            }
        }


        static void AES_EncryptFile(string file)
        {
            string tempFile = file + ".aes";
            FileInfo info = new FileInfo(tempFile);
            if (info.Directory != null && !info.Directory.Exists)
            {
                info.Directory.Create();
            }

            string encryptTitle = FILE_ENCRYPT_TITLE;
            byte[] titleBytes = Encoding.UTF8.GetBytes(encryptTitle);
            byte[] versionBytes = BitConverter.GetBytes(FILE_ENCRYPT_VERSION);

            byte[] fileOriBytes = File.ReadAllBytes(file);
            byte[] bytesEncrypted = AES_Encrypt(fileOriBytes, FILE_ENCRYPT_PASSWORD);

            List<byte> allBytes = new List<byte>();
            allBytes.AddRange(titleBytes);
            allBytes.AddRange(versionBytes);
            allBytes.AddRange(bytesEncrypted);

            File.WriteAllBytes(tempFile, allBytes.ToArray());
        }

        static byte[] AES_Encrypt(byte[] bytesToBeEncrypted, string password)
        {

            byte[] passwordBytes = Encoding.UTF8.GetBytes(password);
            passwordBytes = SHA256.Create().ComputeHash(passwordBytes);
            byte[] encryptedBytes = null;
            // Set your salt here, change it to meet your flavor:
            // The salt bytes must be at least 8 bytes.
            byte[] saltBytes = new byte[] { 2, 3, 1, 6, 5, 6, 7, 8 };
            using (MemoryStream ms = new MemoryStream())
            {
                using (RijndaelManaged AES = new RijndaelManaged())
                {
                    AES.KeySize = 256;
                    AES.BlockSize = 128;
                    var key = new Rfc2898DeriveBytes(passwordBytes, saltBytes, 1000);
                    AES.Key = key.GetBytes(AES.KeySize / 8);
                    AES.IV = key.GetBytes(AES.BlockSize / 8);
                    AES.Mode = CipherMode.CBC;
                    using (var cs = new CryptoStream(ms, AES.CreateEncryptor(), CryptoStreamMode.Write))
                    {
                        cs.Write(bytesToBeEncrypted, 0, bytesToBeEncrypted.Length);
                        cs.Close();
                    }
                    encryptedBytes = ms.ToArray();
                }
            }
            return encryptedBytes;
        }


        static byte[] AES_Decrypt(byte[] bytesToBeDecrypted, string password = FILE_ENCRYPT_PASSWORD)
        {
            string encryptTitle = FILE_ENCRYPT_TITLE;
            byte[] titleBytes = Encoding.UTF8.GetBytes(encryptTitle);

            try
            {
                var fileTitleBytes = bytesToBeDecrypted.Take(titleBytes.Length).ToArray();
                string fileTitleName = Encoding.UTF8.GetString(fileTitleBytes);


                //跳过头文件，
                if (fileTitleName == FILE_ENCRYPT_TITLE)
                {
                    byte[] versionBytes = BitConverter.GetBytes(FILE_ENCRYPT_VERSION); ;
                    byte[] bytes = bytesToBeDecrypted.Skip(titleBytes.Length).Take(versionBytes.Length).ToArray();

                    //版本号不一致，返回出去
                    int version = BitConverter.ToInt32(bytes, 0);
                    if (version != FILE_ENCRYPT_VERSION)
                    {
                        return null;
                    }


                    var encryptDatas = bytesToBeDecrypted.Skip(titleBytes.Length + versionBytes.Length).ToArray();
                    byte[] passwordBytes = Encoding.UTF8.GetBytes(password);
                    passwordBytes = SHA256.Create().ComputeHash(passwordBytes);
                    byte[] decryptedBytes = null;
                    // Set your salt here, change it to meet your flavor:
                    // The salt bytes must be at least 8 bytes.
                    //runtime 需要和编辑器脚本 BuildUtility.AES_Decrypt 中的key需要保持一致
                    byte[] saltBytes = new byte[] { 2, 3, 1, 6, 5, 6, 7, 8 };
                    using (MemoryStream ms = new MemoryStream())
                    {
                        using (RijndaelManaged AES = new RijndaelManaged())
                        {
                            AES.KeySize = 256;
                            AES.BlockSize = 128;
                            var key = new Rfc2898DeriveBytes(passwordBytes, saltBytes, 1000);
                            AES.Key = key.GetBytes(AES.KeySize / 8);
                            AES.IV = key.GetBytes(AES.BlockSize / 8);
                            AES.Mode = CipherMode.CBC;
                            using (var cs = new CryptoStream(ms, AES.CreateDecryptor(), CryptoStreamMode.Write))
                            {
                                cs.Write(encryptDatas, 0, encryptDatas.Length);
                                cs.Close();
                            }

                            decryptedBytes = ms.ToArray();
                        }
                    }

                    return decryptedBytes;

                }

            }
            catch (Exception e)
            {
                return bytesToBeDecrypted;
            }

            return bytesToBeDecrypted;
        }
    }
}
