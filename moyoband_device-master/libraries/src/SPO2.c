#include "SPO2.h"


void tx(int* data, int size, bool* transfer_done){
    *transfer_done=false;
    ret_code_t err_code=nrf_drv_twi_tx(&mTWI,SPO2_ADDRESS,data,size,false);               /**< Fixed sensor address */
    APP_ERROR_CHECK(err_code);
    nrf_delay_ms(1);
    while (transfer_done == false){};
}

void rx(int* data, int size, bool* transfer_done){
    *transfer_done=false;
    ret_code_t err_code = nrf_drv_twi_rx(&mTWI, SPO2_ADDRESS, data, size);
    APP_ERROR_CHECK(err_code);
    nrf_delay_ms(1);
    while (transfer_done == false){};
}

void sensor_off(bool* transfer_done)
{
    uint8_t mode_config[2] = {SPO2_MODE_CONFIG, (1 << 7) };                               /**< LED off */
    tx(&mode_config,2,transfer_done);
}

void sensor_on(bool* transfer_done)
{
    uint8_t mode_config[2] = {SPO2_MODE_CONFIG, SPO2_MC__SPO2MODE};                       /**< SpO2 mode */
    tx(&mode_config,2,transfer_done);
}

void sensor_init(bool* transfer_done)
{

    uint8_t intr_setting_1[2] = {SPO2_INTR_ENABLE_1, 0};                                  /**< Disable fifo interupt */
    tx(&intr_setting_1,2,transfer_done);

    uint8_t intr_setting_2[2] = {SPO2_INTR_ENABLE_2, SPO2_IE2__DIE_TEMP_RDY_EN};          /**< Enable temperature interupt */
    tx(&intr_setting_2,2,transfer_done);


    uint8_t fifo_wr_ptr[2] = {SPO2_FIFO_WR_PTR, 0x00};                                    /**< Reset write pointer */
    tx(&fifo_wr_ptr,2,transfer_done);

    uint8_t ovf_counter[2] = {SPO2_OVF_COUNTER,0x00};                                     /**< Reset overflow counter */
    tx(&ovf_counter,2,transfer_done);

    uint8_t fifo_rd_ptr[2] = {SPO2_FIFO_RD_PTR,0x00};                                     /**< Reset read pointer */
    tx(&fifo_rd_ptr,2,transfer_done);


    uint8_t fifo_config[2] = {SPO2_FIFO_CONFIG, SPO2_FC__SMP_AVE(0x04)  };                /**< Avarage 32 samples into 1 sample */
    tx(&fifo_config,2,transfer_done);

    sensor_on(&transfer_done);
    
    uint8_t spo2_config[2] = {SPO2_SPO2_CONFIG,SPO2_SC__ADC_RESOLUTION(0x03) | SPO2_SC__ADC_RGE(1) | SPO2_SC__SAMPLE_RATE(3)};       /**< ADC range; Samples/s; Pulse width */
    tx(&spo2_config,2,transfer_done);

    uint8_t led1_val[2] = {SPO2_LED1_PA,0x24};                                            /**< LED Current */
    tx(&led1_val,2,transfer_done);

    uint8_t led2_val[2] = {SPO2_LED2_PA,0x24};                                            /**< LED Current */
    tx(&led2_val,2,transfer_done);
 
}


void read_temperature (int8_t* temp_int, int8_t* temp_frac, bool* transfer_done){
  
  uint8_t getTemperature[2] = {SPO2_TEMP_CONFIG, SPO2_TC__TEMP_EN};
  tx( getTemperature, 2, transfer_done);

  read_register(SPO2_TEMP_INTR, temp_int, transfer_done);

  read_register(SPO2_TEMP_FRAC, temp_frac, transfer_done);
  *temp_frac= (*temp_frac & 0x0F)*6.25;

}

void read_register(uint8_t location, uint8_t* output, bool* transfer_done){

  uint8_t source = location;
  tx( &source, 1, transfer_done);
  rx( output, 1, transfer_done);
  
}

void read_fifo_data_spo2(uint32_t* redLED, uint32_t* irLED, uint8_t amount, bool* transfer_done){

  uint8_t pack[6];

  uint8_t source = SPO2_FIFO_DATA;
  tx( &source, 1, transfer_done);
  
  for(uint8_t k=0; k<amount; k++){
    
    rx( pack, 6, transfer_done);
    *redLED =  (pack[0] & 0x03) << 16;
    *redLED += (pack[1]) << 8;
    *redLED += (pack[2]);

    *irLED =  (pack[3] & 0x03) << 16;
    *irLED += (pack[4]) << 8;
    *irLED += (pack[5]);
  
    redLED++;
    irLED++;

  }
}

  