 //I developed a program using the Selenium library and Chrome WebDriver in C# to create a web scraping tool. 
 //This tool checks the availability of a specific event on a website. The program runs in headless mode to avoid 
 //any visual interference. It navigates to the target webpage, extracts the page source, and parses it using 
 //HtmlAgilityPack. By searching for "Agotado" (Spanish for "Sold out") within div elements, the program 
 //determines if the event is available. If it is, it displays "Available!" and can emit a sound using a 
 //Windows Media Player object. The program includes a countdown timer for scheduling regular checks. The 
 //code demonstrates the use of Selenium, WebDriver, and HtmlAgilityPack for web scraping tasks, with potential 
 //for further customization and integration into larger systems.

using System;
using System.IO;
using System.Threading;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using OpenQA.Selenium.Support.Extensions;
using OpenQA.Selenium.Remote;
using HtmlAgilityPack;
using WMPLib;

class Program
{
    static void Main(string[] args)
    {
        var config = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddIniFile("config.ini")
            .Build();

        var chromedriverPath = config.GetSection("Main").Get<string>("chromedriver_path");

        var driver = ConfigureDriver(chromedriverPath);

        while (true)
        {
            Console.Clear();
            CheckAvailability(driver);
            driver.Quit();
            CountdownTimer(1800); // 30 minutes in seconds
        }
    }

    static IWebDriver ConfigureDriver(string chromedriverPath)
    {
        var chromeOptions = new ChromeOptions();
        chromeOptions.AddArgument("--headless");
        chromeOptions.AddArgument("--disable-dev-shm-usage");
        chromeOptions.AddArgument("--disable-blink-features=AutomationControlled");
        chromeOptions.AddArgument("--disable-extensions");
        chromeOptions.AddArgument("--disable-plugins");
        chromeOptions.AddArgument("--start-maximized");
        chromeOptions.AddArgument("--no-sandbox");
        chromeOptions.AddArgument("--disable-infobars");
        chromeOptions.AddArgument("--disable-notifications");
        chromeOptions.AddArgument("--disable-popup-blocking");
        chromeOptions.AddExcludedArgument("enable-automation");
        chromeOptions.AddAdditionalCapability("useAutomationExtension", false);

        var service = ChromeDriverService.CreateDefaultService(chromedriverPath);
        var driver = new ChromeDriver(service, chromeOptions);

        return driver;
    }

    static void CheckAvailability(IWebDriver driver)
    {
        try
        {
            // Open the web page
            driver.Navigate().GoToUrl("https://wmw.allaccess.com.ar/event/taylor-swift-the-eras-tour");

            // Wait for the page to fully load
            Thread.Sleep(5000);

            // Extract the page source
            var pageSource = driver.PageSource;

            // Create HtmlDocument object for parsing the page source
            var htmlDoc = new HtmlDocument();
            htmlDoc.LoadHtml(pageSource);

            // Find all div elements on the page
            var divElements = htmlDoc.DocumentNode.Descendants("div");

            // Check if any div contains the text "Agotado"
            var agotadoFound = false;
            foreach (var div in divElements)
            {
                if (div.InnerText.Contains("Agotado"))
                {
                    agotadoFound = true;
                    break;
                }
            }

            // Emit a sound if "Agotado" text is not found
            if (!agotadoFound)
            {
                Console.WriteLine("Available!");
                // Add your code here to emit a sound
                var player = new WindowsMediaPlayer();
                player.URL = @"C:\path\to\your\sound\file.mp3";
                player.controls.play();
            }
        }
        catch (Exception e)
        {
            Console.WriteLine("An error occurred: " + e.Message);
        }
    }

    static void CountdownTimer(int seconds)
    {
        while (seconds > 0)
        {
            var minutes = seconds / 60;
            var secs = seconds % 60;
            var timer = string.Format("{0:00}:{1:00}", minutes, secs);
            Console.WriteLine("Next check in: " + timer);
            Thread.Sleep(1000);
            seconds
