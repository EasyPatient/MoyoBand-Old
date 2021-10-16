#ifndef SPO2_H__
#define SPO2_H__

#include "nrf_drv_twi.h"
#include "app_error.h"
#include "nrf_delay.h"
#include "bsp.h"
#include "nrf_log.h"
#ifdef  BOARD_PCA10059
  #define ARDUINO_SCL_PIN NRF_GPIO_PIN_MAP(0, 13)
  #define ARDUINO_SDA_PIN NRF_GPIO_PIN_MAP(0, 15)
#endif

#define SPO2_ADDRESS              0x57                   /**< Sensor adress */

#define SPO2_INTR_STATUS_1        0x00
  #define SPO2_IS1__A_FULL          1 << 7                   /**< Almost full FIFO */
  #define SPO2_IS1__PPG_RDY         1 << 6                   /**< New sample ready */
  #define SPO2_IS1__ALC_OVF         1 << 5                   /**< Ambient light is affecting the output of the ADC */
  #define SPO2_IS1__PWR_RDY         1 << 0

#define SPO2_INTR_STATUS_2        0x01
  #define SPO2_IS2__DIE_TEMP_RDY     1 << 1                  /**< New temparature sample ready to read */ 

#define SPO2_INTR_ENABLE_1        0x02                   /**< Enable each type of interupt */
  #define SPO2_IE1__A_FULL_EN        1 << 7
  #define SPO2_IE1__PPG_RDY_EN       1 << 6
  #define SPO2_IE1__ALC_OVF_EN       1 << 5 
         
#define SPO2_INTR_ENABLE_2        0x03
  #define SPO2_IE2__DIE_TEMP_RDY_EN  1<<1

#define SPO2_FIFO_WR_PTR          0x04                   /**< Points to the location where the MAX30102 writes the next sample */
#define SPO2_OVF_COUNTER          0x05             
#define SPO2_FIFO_RD_PTR          0x06             
#define SPO2_FIFO_DATA            0x07                   /**< Hold up to 32 samples of data */

#define SPO2_FIFO_CONFIG          0x08
  #define SPO2_FC__SMP_AVE(code)      code << 5                  /**< Average 32 samples of data into one sample */
  #define SPO2_FC__FIFO_ROLLOVER_EN   1 << 4                  /**< When FIFO is filled - start writing again */
  #define SPO2_FC__FIFO_A_FULL(empty) empty                /**< Set number of free data samples to write into in FIFO */

#define SPO2_MODE_CONFIG          0x09
  #define SPO2_MC__SHDN              1 << 7                  /**< Power-save mode -  all registers retain their values */
  #define SPO2_MC__RESET             1 << 6                  /**< Reset to power-on-state */
  #define SPO2_MC__HRMODE            2
  #define SPO2_MC__SPO2MODE          3
  #define SPO2_MC__MULTILEDMODE      7

#define SPO2_SPO2_CONFIG          0x0A 
  #define SPO2_SC__ADC_RGE(code)     code << 5               /**< Set ADC current */
  #define SPO2_SC__SAMPLE_RATE(code) code << 2               /**< Set number of samples/sec */
  #define SPO2_SC__ADC_RESOLUTION(code) code 
         
#define SPO2_LED1_PA              0x0C                  
#define SPO2_LED2_PA              0x0D
#define SPO2_LED_PA__CURRENT(code) code                  /**< Current level of rach LED */

#define SPO2_PILOT_PA             0x10                 
#define SPO2_MULTI_LED_CTRL1      0x11          
#define SPO2_MULTI_LED_CTRL2      0x12           
#define SPO2_TEMP_INTR            0x1F                 
#define SPO2_TEMP_FRAC            0x20                 
#define SPO2_TEMP_CONFIG          0x21
  #define SPO2_TC__TEMP_EN          1 << 0                   /**< Single temperature sample */
#define SPO2_PROX_INT_THRESH      0x30           
#define SPO2_REV_ID               0xFE                    
#define SPO2_PART_ID              0xFF                   /**< 0x15 */

#define STORAGE_SIZE              100

#ifdef __cplusplus
extern "C" {
#endif

static volatile bool transfer_done = false;

/* TWI instance ID. */
#if TWI0_ENABLED
  #define TWI_INSTANCE_ID 0                                /**< Default is 0 */
#endif
/* TWI instance. */
static const nrf_drv_twi_t mTWI = NRF_DRV_TWI_INSTANCE(TWI_INSTANCE_ID);

/**@brief Send data through TWI (I2C)
 *
 * @param[in]   size    Sending data size
 * @param[in]   bool*   Indicates end of transfer
 */
void tx(int* data, int size, bool* transfer_done);

/**@brief Recive data through TWI (I2C)
 *
 * @param[in]   size    Reading data size
 * @param[in]   bool*   Indicates end of transfer
 */
void rx(int* data, int size, bool*);


/**@brief Turn on sensor power. It is used to power menagement **/
void sensor_off(bool* transfer_done);

void sensor_on(bool* transfer_done);

/**@brief Initial sensor configuration
 *
 * @param[in]   bool*   Indicates end of transfer
 */
void sensor_init(bool*);

/**@brief Read temperature and store it in variables
 *
 * @param[in]   tempInt, tempFrac  Temperature - int part and fractal part
 * @param[in]   bool*     Indicates end of transfer
 */
void read_temperature (int8_t* tempInt, int8_t* tempFrac, bool*);

/**@brief Read particular sensor's register
 *
 * @param[in]   location  Register's address
 * @param[in]   output    Value read
 * @param[in]   bool*     Indicates end of transfer
 */
void read_register(uint8_t location, uint8_t* output, bool* );

/**@brief Read many sensor samples
 *
 * @param[in]   redLED, irLED  Arrays for sensor samples
 * @param[in]   amount     Amount of samples to read
 * @param[in]   bool*      Indicates end of transfer
 */
void read_fifo_data_spo2(uint32_t* redLED, uint32_t* irLED, uint8_t amount, bool*);
#ifdef __cplusplus
}
#endif

#endif