//-------------------------------------------------------------------------------------------
/*! \file    cv2-capture_fps3.cpp
    \brief   Capture with specific FPS by cap_libv4l_2.cpp (modified version of cap_libv4l.cpp in OpenCV 2.4)
    \author  Akihiko Yamaguchi, info@akihikoy.net
    \version 0.1
    \date    Jul.22, 2016

g++ -g -Wall -O2 -o cv2-capture_fps3.out cv2-capture_fps3.cpp cv2e/cap_libv4l_2.cpp -I/usr/include/eigen3 -lopencv_core -lopencv_highgui -lv4l1 -lv4l2
g++ -g -Wall -O2 -o cv2-capture_fps3.out cv2-capture_fps3.cpp cv2e/cap_libv4l_2.cpp -I$HOME/.local/include -I/usr/include/eigen3 -L$HOME/.local/lib -Wl,-rpath=$HOME/.local/lib -lopencv_core -lopencv_highgui -lv4l1 -lv4l2

*/
//-------------------------------------------------------------------------------------------
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <cstdio>
#include <sys/time.h>  // gettimeofday
//-------------------------------------------------------------------------------------------
CvCapture* cvCreateCameraCapture_V4L_2(int index);
//-------------------------------------------------------------------------------------------
namespace loco_rabbits
{

#define CV_CAP_FPS(numerator, denominator)  ((double)numerator*1e8+(double)denominator)
class VideoCapture2 : public cv::VideoCapture
{
public:
  CV_WRAP VideoCapture2() : cv::VideoCapture() {}
  CV_WRAP VideoCapture2(const std::string& filename) : cv::VideoCapture(filename) {}
  CV_WRAP VideoCapture2(int device) : cv::VideoCapture(device) {}
  ~VideoCapture2()  {}

  /*override*/ bool open(int device)
    {
      cap= cvCreateCameraCapture_V4L_2(device);
      return isOpened();
    }
};


inline double GetCurrentTime(void)
{
  struct timeval time;
  gettimeofday (&time, NULL);
  return static_cast<double>(time.tv_sec) + static_cast<double>(time.tv_usec)*1.0e-6;
  // return ros::Time::now().toSec();
}
//-------------------------------------------------------------------------------------------

struct TFPSEstimator
{
  double Alpha;
  double FPS;
  double TimePrev;
  TFPSEstimator(const double &init_fps=10.0, const double &alpha=0.05);
  void Step();
};
//-------------------------------------------------------------------------------------------
TFPSEstimator::TFPSEstimator(const double &init_fps, const double &alpha)
  :
    Alpha (alpha),
    FPS (init_fps),
    TimePrev (-1.0)
{
}
void TFPSEstimator::Step()
{
  if(TimePrev<0.0)
  {
    TimePrev= GetCurrentTime();
  }
  else
  {
    double new_fps= 1.0/(GetCurrentTime()-TimePrev);
    if(new_fps>FPS/20.0 && new_fps<FPS*20.0)  // Removing outliers (e.g. pause/resume)
      FPS= Alpha*new_fps + (1.0-Alpha)*FPS;
    TimePrev= GetCurrentTime();
  }
}
//-------------------------------------------------------------------------------------------


}
//-------------------------------------------------------------------------------------------
using namespace std;
// using namespace boost;
using namespace loco_rabbits;
//-------------------------------------------------------------------------------------------
// #define print(var) PrintContainer((var), #var"= ")
// #define print(var) std::cout<<#var"= "<<(var)<<std::endl
//-------------------------------------------------------------------------------------------

int main(int argc, char**argv)
{
  int cam_id(0);
  VideoCapture2 cap(cam_id);
  if(argc==2)
  {
    cap.release();
    cam_id= atoi(argv[1]);
    cap.open(cam_id);
  }
  if(!cap.isOpened())  // check if we succeeded
  {
    std::cerr<<"no camera!"<<std::endl;
    return -1;
  }
  std::cerr<<"camera opened"<<std::endl;

  // set resolution
  cap.set(CV_CAP_PROP_FOURCC,CV_FOURCC('M','J','P','G'));
  // cap.set(CV_CAP_PROP_FRAME_WIDTH, 1920);
  // cap.set(CV_CAP_PROP_FRAME_HEIGHT, 1080);
  // cap.set(CV_CAP_PROP_FOURCC,CV_FOURCC('Y','U','Y','V'));
  // cap.set(CV_CAP_PROP_AUTO_EXPOSURE, 0);
  cap.set(CV_CAP_PROP_EXPOSURE, 0.0);
  cap.set(CV_CAP_PROP_GAIN, 0.0);

  // cap.set(CV_CAP_PROP_FRAME_WIDTH, 640);
  // cap.set(CV_CAP_PROP_FRAME_HEIGHT, 480);
  // cap.set(CV_CAP_PROP_FRAME_WIDTH, 320);
  // cap.set(CV_CAP_PROP_FRAME_HEIGHT, 240);
  // cap.set(CV_CAP_PROP_FPS, CV_CAP_FPS(1,15));  // Works with built-in camera of T440p
  // cap.set(CV_CAP_PROP_FPS, CV_CAP_FPS(513,61612));  // Doesn't work with ELP USBFHD01M-L180 as we are using YUYV? BGR3?
  cap.set(CV_CAP_PROP_FRAME_WIDTH, 800);
  cap.set(CV_CAP_PROP_FRAME_HEIGHT, 600);
  cap.set(CV_CAP_PROP_FPS, CV_CAP_FPS(1,60));  // Works with ELP USBFHD01M-L180

  TFPSEstimator fps;
  int show_fps(0);
  cv::namedWindow("camera",1);
  cv::Mat frame;
  for(;;)
  {
    cap >> frame; // get a new frame from camera
    cv::imshow("camera", frame);
    fps.Step();
    if(show_fps==0)
    {
      std::cerr<<"FPS: "<<fps.FPS<<std::endl;
      show_fps= fps.FPS*4;
    }
    --show_fps;
    int c(cv::waitKey(1));
    if(c=='\x1b'||c=='q') break;
    // usleep(10000);
  }
  // the camera will be deinitialized automatically in VideoCapture destructor
  return 0;
}
//-------------------------------------------------------------------------------------------
