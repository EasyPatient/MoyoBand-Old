#ifndef MOYO_BLE__
#define MOYO_BLE__

#include "stdint.h"
#include "ble.h"
#include "nrf_ble_gatt.h"
#include "nrf_sdh_ble.h"
#include "ble_srv_common.h"

#define BLE_UUID_MOYO_SERVICE_UUID        0x3333  // pulse oximeter
#define BLE_UUID_MOYO_HR                  0x2A37
#define BLE_UUID_MOYO_OXIMETRY            0x2A62
#define BLE_UUID_MOYO_TEMPERATURE         0x2A6E
#define BLE_MOYO_BLE_OBSERVER_PRIO 2


#define BLE_MOYO_DEF(_name)                                                                         \
static ble_moyo_t _name;                                                                            \
NRF_SDH_BLE_OBSERVER(_name ## _obs,                                                                 \
                     BLE_MOYO_BLE_OBSERVER_PRIO,                                                    \
                     ble_moyo_on_ble_evt, &_name)                                                   


typedef struct ble_moyo_s ble_moyo_t;

/**@brief Moyo Service event type. */
typedef enum
{
    BLE_MOYO_EVT_NOTIFICATION_ENABLED,   /**< Moyo value notification enabled event. */
    BLE_MOYO_EVT_NOTIFICATION_DISABLED   /**< Moyo value notification disabled event. */
} ble_moyo_evt_type_t;

/**@brief Moyo Service event. */
typedef struct
{
    ble_moyo_evt_type_t evt_type;    /**< Type of event. */
} ble_moyo_evt_t;


/**@brief Moyo Service event handler type. */
typedef void (*ble_moyo_evt_handler_t) (ble_moyo_t * p_moyo, ble_moyo_evt_t * p_evt);

/**@brief Moyo connection struct. */
typedef struct
{
    ble_moyo_evt_handler_t      evt_handler;
    security_req_t              write_sec;
    security_req_t              read_sec;
    uint8_t                     init_value;

} ble_moyo_init_t; 

/**@brief Moyo data struct. Contains all data from sensor. */
struct moyo_data
{
    uint8_t                     hr_data;
    uint8_t                     oximetry;
    uint8_t                     temperature[2];

};

/**@brief Main structure for Moyo BLE connection. with all handlers and data. */
struct ble_moyo_s
{
    ble_moyo_evt_handler_t      evt_handler;
    uint16_t                    service_handle;
    ble_gatts_char_handles_t    moyo_hr_handle;
    ble_gatts_char_handles_t    moyo_oximetry_handle;
    ble_gatts_char_handles_t    moyo_temperature_handle;
    uint16_t                    conn_handle;
    uint8_t                     uuid_type;
    struct moyo_data            moyo_data;
    
};


/**@brief Adding characteristics. It makes ble_moyo_init more clear.
 *
 * @param[in]   p_moyo          Main moyo structure with data and all handlers
 * @param[in]   p_moyo_init     Connection Settings
 *
 * @return      uint32_t        Error code
 */
uint32_t ble_moyo_char_add(ble_moyo_t * p_moyo, ble_moyo_init_t const * p_moyo_init);

/**@brief Initialize BLE connections with services and characteristics.
 *
 * @param[in]   p_moyo          Main moyo structure with data and all handlers
 * @param[in]   p_moyo_init     Connection Settings
 *
 * @return      uint32_t        Error code
 */
uint32_t ble_moyo_init(ble_moyo_t * p_moyo, const ble_moyo_init_t * p_moyo_init);

/**@brief Update values in GATTS connection.
 *
 * @param[in]   p_moyo          Main moyo structure with data and all handlers
 *
 * @return      uint32_t        Error code
 */
uint32_t ble_moyo_update(ble_moyo_t * p_moyo);


/**@brief Handling BLE event
 *
 * @param[in]   p_moyo          Main moyo structure with data and all handlers
 * @param[in]   p_moyo_init     Connection handler
 */
void ble_moyo_on_ble_evt(ble_moyo_t * p_moyo, ble_evt_t const * p_ble_evt);
#endif 