using System.Windows;

namespace DRYRUN
{
    public partial class App : System.Windows.Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            // Create window but do NOT show it
            
            MainWindow window = new MainWindow();
            window.Show();
        }
    }
}
